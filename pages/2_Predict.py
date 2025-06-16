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

# -------------------- Input Section on Main Page --------------------

st.header("Compound Input")

# Create columns for better layout
col1, col2 = st.columns([1, 3])

with col1:
    search_mode = st.radio("Search by:", ["Name", "SMILES"], index=0)

name_input = None
smiles_input = None

with col2:
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

# Place the predict button below the input section
input_ready = (smiles_input if search_mode == "SMILES" else name_input)
predict_button = st.button("Predict Toxicity", disabled=not input_ready,
                          type="primary", use_container_width=True)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# -------------------- Prediction Section --------------------

# if predict_button:
#     smiles = ""
#     common_name = ""
#     iupac_name = ""

#     if search_mode == "SMILES":
#         smiles = smiles_input
#     elif search_mode == "Name":
#         if name_input:
#             if name_type == "Common Name":
#                 common_name = name_input
#             else:
#                 iupac_name = name_input

#     if any([smiles, common_name, iupac_name]):
#         with st.spinner("🧪 Predicting toxicity..."):
#             try:
#                 data = {
#                     "iupac_name": iupac_name,
#                     "common_name": common_name,
#                     "smiles": smiles,
#                 }
#                 response = requests.post("http://localhost:8000/predict/", json=data)

#                 if response.status_code == 200:
#                     st.success(":white_check_mark: Prediction completed successfully!")

#                     # Display results in a more organized way
#                     st.subheader("Prediction Results")
#                     results = response.json()

#                     # You can customize how you display the results here
#                     st.json(results)  # or create a more detailed display

#                 else:
#                     st.error(f":x: Prediction failed with status code {response.status_code}")
#             except Exception as e:
#                 st.error(f":x: Cannot connect to server: {e}")
#     else:
#         st.warning("Please provide a valid input.")

data = {
                   "compound": 'NCGC00261900-01',
                   "target": 'SR.MMP',
                 }
response = requests.post("http://localhost:8000/predict/", json=data)

st.write(response.json())
