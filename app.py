import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
import requests


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
    if search_mode == "SMILES":
        iupac_name = ""
        common_name = ""
        smiles = smiles_input
    elif search_mode == "Name":
        if name_type == "Common Name":
            iupac_name = ""
            common_name = name_input
            smiles = ""
        else :
            iupac_name = name_input
            common_name = ""
            smiles = ""

if predict_button:
    try:
        data = {"iupac_name": iupac_name,  "common_name": common_name, "smiles": smiles,}
        response = requests.post("http://localhost:8000/predict/", json=data)

        if response.status_code == 200:
            st.success(":white_check_mark: Data submitted successfully!")
            st.write(response.json())
        else:
            st.error(":x: Submission failed")
    except:
        st.error(":x: Cannot connect to server")
else:
    st.warning("Please fill all fields")

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
