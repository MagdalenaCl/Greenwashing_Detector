import streamlit as st
import pandas as pd
import plotly.express as px
import json
import base64

# --- Daten laden ---
df = pd.read_csv("greenwashing_classification.csv")
with open("similarity_data.json", "r", encoding="utf-8") as f:
    similarity_data = json.load(f)

# --- Page Setup ---
st.set_page_config(layout="wide", page_title="Greenwashing Dashboard", initial_sidebar_state="collapsed")
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_of_bin_file("Greenwashing_Detector_Logo.png")

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

# --- Semantischer Vergleich ---
st.markdown("### Semantischer Vergleich: Bericht vs. Presseartikel")
artikel_sätze = [item["artikel_chunk"][:100] + "…" for item in similarity_data]
auswahl = st.selectbox("Presseartikel-Satz auswählen", options=list(enumerate(artikel_sätze)), format_func=lambda x: x[1])
index = auswahl[0]
ausgewählter = similarity_data[index]

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Presseartikel:**\n\n{ausgewählter['artikel_chunk']}")
with col2:
    st.markdown("**Top ähnliche Passagen im Bericht:**")
    for match in ausgewählter["top_matches"]:
        st.markdown(f"> **Score:** {match['similarity']:.2f}")
        st.markdown(match["bericht_text"])
        st.markdown("---")

st.divider()

# --- KPI Verteilung ---
st.markdown("### Verteilung der Klassifikationen")
label_counts = df["label"].value_counts().reset_index()
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
    selected_label = st.selectbox("Kategorie", ["Alle"] + sorted(df["label"].unique()))

filtered_df = df[df["score"] >= min_score]
if selected_label != "Alle":
    filtered_df = filtered_df[filtered_df["label"] == selected_label]

st.success(f"{len(filtered_df)} passende Aussagen gefunden")

for i, row in filtered_df.head(20).iterrows():
    with st.expander(f"{row['label'].capitalize()} – Score: {row['score']:.2f}"):
        st.write(row["text"])

st.divider()

# --- Score Verteilung ---
st.markdown("### Score-Verteilung")
fig_hist = px.histogram(df, x="score", nbins=20, color="label",
                        color_discrete_sequence=farben)
st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# --- Export ---
st.markdown("### Export")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="CSV herunterladen",
    data=csv,
    file_name="greenwashing_gefiltert.csv",
    mime="text/csv"
)