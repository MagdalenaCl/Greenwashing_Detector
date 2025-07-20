import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("greenwashing_classification.csv")

st.set_page_config(page_title="Greenwashing-Analyse", layout="wide")

st.title("Greenwashing-Klassifikation")
st.markdown("Analyse von Aussagen aus dem Nachhaltigkeitsbericht – kategorisiert nach Greenwashing-Potenzial.")

# --- Tortendiagramm
st.header("Verteilung der Klassifikationen")
label_counts = df["label"].value_counts().reset_index()
label_counts.columns = ["label", "count"]
fig = px.pie(label_counts, names="label", values="count", hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig, use_container_width=True)

# --- Filteroptionen
st.header("Aussage-Explorer")
min_score = st.slider("Mindest-Score", 0.0, 1.0, 0.6, 0.01)
selected_label = st.selectbox("Kategorie", ["Alle"] + sorted(df["label"].unique()))

filtered_df = df[df["score"] >= min_score]
if selected_label != "Alle":
    filtered_df = filtered_df[filtered_df["label"] == selected_label]

st.write(f"{len(filtered_df)} passende Aussagen gefunden")

# --- Anzeigen
for i, row in filtered_df.head(10).iterrows():
    st.markdown(f"**Kategorie:** {row['label']}")
    st.markdown(f"**Score:** {row['score']:.2f}")
    st.markdown(f"**Text:** {row['text']}")
    st.markdown("---")