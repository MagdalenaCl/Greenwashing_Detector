import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import glob

# --- Daten laden ---
classification_folder = "results_classification"
all_csv_files = glob.glob(os.path.join(classification_folder, "*.csv"))

dfs = []
for file in all_csv_files:
    try:
        df = pd.read_csv(file)
        dfs.append(df)
    except Exception as e:
        print(f"Fehler beim Laden von {file}: {e}")

if not dfs:
    st.error("Keine Klassifikationsdaten gefunden.")
    st.stop()

df = pd.concat(dfs, ignore_index=True)
df["year"] = df["year"].astype(str)

# --- Page Setup ---
st.set_page_config(layout="wide", page_title="Greenwashing Dashboard", initial_sidebar_state="collapsed")
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_of_bin_file("images\Greenwashing_Detector_Logo.png")

st.markdown(f"""
<div class="header">
    <div class="header-left">
        <h2>Greenwashing Dashboard</h2>
    </div>
    <div class="header-right">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" />
    </div>
</div>
""", unsafe_allow_html=True)

# --- Filter: Unternehmen und Jahr ---
st.sidebar.markdown("### Filter")
companies = sorted(df["company"].unique())
selected_company = st.sidebar.selectbox("Unternehmen auswählen", ["Alle"] + companies)
available_years = df["year"].unique() if selected_company == "Alle" else df[df["company"] == selected_company]["year"].unique()
selected_year = st.sidebar.selectbox("Jahr auswählen", sorted(available_years))

# --- Filter anwenden ---
if selected_company == "Alle":
    df_filtered = df[df["year"] == selected_year]
else:
    df_filtered = df[(df["company"] == selected_company) & (df["year"] == selected_year)]

farben = ["#81c784", "#ffd54f", "#ffb74d", "#e57373"]

# --- Wenn "Alle": Nur Vergleichsdiagramm anzeigen ---
if selected_company == "Alle":
    st.markdown(f"### Vergleich der Klassifikationen (alle Unternehmen, {selected_year})")
    label_counts = df_filtered.groupby("company")["label"].value_counts().unstack().fillna(0)

    fig = px.bar(label_counts, barmode="group", text_auto=True, color_discrete_sequence=farben)
    fig.update_layout(xaxis_title="Unternehmen", yaxis_title="Anzahl", legend_title="Label")
    st.plotly_chart(fig, use_container_width=True)

else:
    # --- Bewertungstabelle ---
    evaluation_path = f"results_chatgpt/comparison_{selected_company.replace(' ', '')}_{selected_year}.csv"

    if os.path.exists(evaluation_path):
        st.markdown(f"### Bewertung der Nachhaltigkeitsversprechen ({selected_company}, {selected_year})")
        evaluation_df = pd.read_csv(evaluation_path, sep=';', index_col=0)
        evaluation_df.columns = evaluation_df.columns.str.strip()

        def traffic_light_color(ampel):
            return {
                "🟢": "background-color: #c8e6c9",
                "🟡": "background-color: #fff9c4",
                "🔴": "background-color: #ffcdd2"
            }.get(ampel, "")

        styled = evaluation_df.style.map(traffic_light_color, subset=["Ampel"])
        st.dataframe(styled, use_container_width=True)
    else:
        st.info(f"ℹ️ Für {selected_company} im Jahr {selected_year} liegt noch keine Bewertungstabelle vor.")

    st.divider()

# --- KPI Verteilung ---
st.markdown(f"### Verteilung der Klassifikationen ({selected_company}, {selected_year})")
label_counts = df_filtered["label"].value_counts().reset_index()
label_counts.columns = ["Label", "Anzahl"]
farben = ["#81c784", "#ffd54f", "#ffb74d", "#e57373"]

kpi1, kpi2 = st.columns(2)
with kpi1:
    fig_pie = px.pie(label_counts, names="Label", values="Anzahl", hole=0.5,
                     color_discrete_sequence=farben)
    st.plotly_chart(fig_pie, use_container_width=True)
with kpi2:
    fig_bar = px.bar(label_counts, x="Label", y="Anzahl",
                     color="Label", text="Anzahl",
                     color_discrete_sequence=farben)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# --- Aussage-Explorer ---
st.markdown("### Aussage-Explorer")
col1, col2 = st.columns([1, 3])
with col1:
    min_score = st.slider("Mindest-Sicherheit", 0.0, 1.0, 0.6, 0.01)
with col2:
    selected_label = st.selectbox("Kategorie", ["Alle"] + sorted(df_filtered["label"].unique()))

explorer_df = df_filtered[df_filtered["score"] >= min_score]
if selected_label != "Alle":
    explorer_df = explorer_df[explorer_df["label"] == selected_label]

st.success(f"{len(explorer_df)} passende Aussagen gefunden")

for i, row in explorer_df.head(20).iterrows():
    with st.expander(f"{row['label'].capitalize()} – Score: {row['score']:.2f}"):
        st.write(row["text"])

st.divider()

# --- Score Verteilung ---
st.markdown("### Score-Verteilung")
fig_hist = px.histogram(df_filtered, x="score", nbins=20, color="label",
                        color_discrete_sequence=farben)
st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# --- Export ---
st.markdown(f"### Export ({selected_company}, {selected_year})")
csv = explorer_df.to_csv(index=False).encode("utf-8")
csv_filename = f"{selected_company}_{selected_year}_gefiltert.csv".replace(" ", "_")

st.download_button(
    label="CSV herunterladen",
    data=csv,
    file_name=csv_filename,
    mime="text/csv"
)
