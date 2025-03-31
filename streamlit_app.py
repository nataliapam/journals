
import streamlit as st
import pandas as pd
import os

# Cargar usuarios autorizados desde Secrets
AUTHORIZED_USERS = [
    os.getenv("USER1"),
    os.getenv("USER2"),
    os.getenv("USER3"),
    os.getenv("USER4"),
    os.getenv("USER5"),
    os.getenv("USER6"),
    os.getenv("USER7"),
    os.getenv("USER8"),
    os.getenv("USER9"),
    os.getenv("USER10"),
]
AUTHORIZED_USERS = [u for u in AUTHORIZED_USERS if u]

# --- LOGIN ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔐 Login Required")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        credential = f"{email}:{password}"
        if credential in AUTHORIZED_USERS:
            st.session_state['authenticated'] = True
            st.success("Login successful! Please wait...")
            st.stop()
        else:
            st.error("Invalid email or password.")
    st.stop()

# --- APP CONTENT STARTS HERE ---


import streamlit as st
import pandas as pd

# Page config with favicon
st.set_page_config(
    page_title="Journal Ratings Finder",
    page_icon="favicon.ico"
)

# Custom CSS for layout and mobile optimizations
custom_css = """
    <style>
    #MainMenu, header, footer {
        visibility: hidden;
    }

    .block-container:has(> footer) {
        padding-bottom: 0 !important;
    }

    .scroll-container {
        overflow-x: auto;
    }

    @media only screen and (max-width: 768px) {
        .main .block-container {
            padding-top: 0.5rem !important;
        }
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("Journals.xlsx")
    df["Normalized_Title"] = df["Revista"].str.lower().str.strip()
    return df

df = load_data()
unique_titles = df["Revista"].sort_values().unique()

st.title("Academic Journal Ratings Finder")

with st.expander("Journal ratings from five major sources", expanded=True):
    st.markdown("""
    For each origin, the ratings are shown in descending order (best to worst):

    - **AJG**: 4*, 4, 3, 2, 1  
    - **CNRS**: 1*, 1, 2, 3, 4  
    - **CNU**: A, B, C  
    - **VHB**: A+, A, B, C, D  
    - **ABDC**: A*, A, B, C
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
        pivot = results.pivot_table(index="Revista", columns="Origen", values="Rating", aggfunc="first").reset_index()

        # Ensure all columns are present
        full_columns = ["Revista", "AJG", "CNRS", "CNU", "VHB", "ABDC"]
        for col in full_columns:
            if col not in pivot.columns:
                pivot[col] = ""

        pivot = pivot[full_columns]

        # Add scrollable container
        st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
        st.dataframe(pivot, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download
        csv = pivot.to_csv(index=False).encode('utf-8')
        st.download_button("Download results as CSV", csv, "journal_ratings_results.csv", "text/csv")
    else:
        st.warning("No matches found.")
