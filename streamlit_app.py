
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("REVISTAS_LISTADO_DEPURADO_ORDENADO_LIMPIO.xlsx")
    df["Normalized_Title"] = df["Revista"].str.lower().str.strip()
    return df

df = load_data()
unique_titles = df["Revista"].sort_values().unique()

st.title("Academic Journal Ratings Finder")

st.markdown("""
Search and compare journal rankings from five major sources:

- **AJG**: 4 (highest), 3, 2, 1
- **CNRS**: 1*, 1, 2, 3, 4 (1* is highest)
- **CNU**: A (highest), B, C
- **VHB**: A+ (highest), A, B, C, D
- **ABDC**: A* (highest), A, B, C
""")

# Multiselect input
selected_journals = st.multiselect(
    "Select one or more journal titles:",
    options=unique_titles,
    help="Start typing to filter the list. You can select multiple journals."
)

if selected_journals:
    normalized_selection = [j.lower().strip() for j in selected_journals]
    results = df[df["Normalized_Title"].isin(normalized_selection)]
    
    if not results.empty:
        table = results.pivot_table(index="Revista", columns="Origen", values="Rating", aggfunc="first").reset_index()

        # Reorder columns
        desired_order = ["Revista", "AJG", "CNRS", "CNU", "VHB", "ABDC"]
        existing_columns = [col for col in desired_order if col in table.columns]
        table = table[existing_columns]

        st.dataframe(table, use_container_width=True)

        # Download
        csv = table.to_csv(index=False).encode('utf-8')
        st.download_button("Download results as CSV", csv, "journal_ratings_results.csv", "text/csv")
    else:
        st.warning("No matches found.")
