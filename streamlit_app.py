
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("REVISTAS_LISTADO_DEPURADO_ORDENADO_LIMPIO.xlsx")
    df["Normalized_Title"] = df["Revista"].str.lower().str.strip()
    return df

df = load_data()

st.title("Academic Journal Ratings Finder")
st.markdown("Search and compare journal rankings across AJG, CNRS, CNU, VHB, and ABDC.")

# User input
search_input = st.text_area("Enter one or more journal names (one per line):").strip()

if search_input:
    # Process input
    queries = [q.lower().strip() for q in search_input.split("\n") if q.strip()]
    
    # Find matches
    results = df[df["Normalized_Title"].apply(lambda x: any(q in x for q in queries))]
    
    if not results.empty:
        # Pivot table to show ratings by source
        table = results.pivot_table(index="Revista", columns="Origen", values="Rating", aggfunc="first").reset_index()

        # Reorder columns
        desired_order = ["Revista", "AJG", "CNRS", "CNU", "VHB", "ABDC"]
        existing_columns = [col for col in desired_order if col in table.columns]
        table = table[existing_columns]

        # Display
        st.dataframe(table, use_container_width=True)

        # Download
        csv = table.to_csv(index=False).encode('utf-8')
        st.download_button("Download results as CSV", csv, "journal_ratings_results.csv", "text/csv")
    else:
        st.warning("No matches found.")
