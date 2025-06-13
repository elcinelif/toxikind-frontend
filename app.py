import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox


def load_data():
    return pd.read_pickle('media/compounds.pkl')

df = load_data()

# Prepare autocomplete for SMILES
smiles_list = df["smiles"].dropna().unique().tolist()

def search_smiles(term: str):
    term = term.strip().upper()
    return [s for s in smiles_list if term in s.upper()]

st.markdown(
    """
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style="
            font-size: 4rem;
            font-weight: 700;
            color: #006d77;
            margin-bottom: 0.2em;
        ">
            ToxiKind 🤍
        </h1>
        <p style="
            font-size: 1.2rem;
            font-weight: 400;
            color: #595959;
            margin-top: 0;
        ">
            An AI-Based Toxicity Prediction Tool to Minimize Harm
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.header("Input")

    # Choose search mode
    search_mode = st.radio("Search by:", ["Name", "SMILES"], index=0)

    name_input = None
    smiles_input = None

    if search_mode == "Name":
        name_type = st.selectbox("Name type:", ["Common Name", "IUPAC Name"])
        if name_type == "Common Name":
            names = df["title"].dropna().unique().tolist()
        else:
            names = df["iupac_name"].dropna().unique().tolist()

        name_input = st.selectbox(f"Select a {name_type.lower()}:", [""] + sorted(names))

    else:
        smiles_input = st_searchbox(
            search_smiles,
            key="smiles_searchbox",
            placeholder="Type or paste a SMILES string..."
        )

    predict_button = st.button("Predict")

# Prediction logic
if predict_button:
    if (name_input and name_input != "") or (smiles_input and smiles_input != ""):
        query = name_input if name_input else smiles_input
        st.success(f"Prediction triggered using: {query}")
    else:
        st.warning("Please select a name or enter a SMILES string before predicting.")


# -------------------- Footer ----------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray;'>
        Built with 🤍 by
        <a href="https://github.com/bartdutkiewicz" target="_blank">bartdutkiewicz</a>,
        <a href="https://github.com/elcinelif" target="_blank">elcinelif</a>,
        <a href="https://github.com/kostovI" target="_blank">kostovI</a>, and
        <a href="https://github.com/madpythonista" target="_blank">madpythonista</a><br>
        For now, predicts Tox21 test set only.
    </div>
    """,
    unsafe_allow_html=True
)
