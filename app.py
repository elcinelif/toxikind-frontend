import streamlit as st
import pandas as pd

 #Load compound data

#def load_data():
 #   return pd.read_csv("tox21_test_with_names.csv")

#data = load_data()


# Sidebar
st.sidebar.title("ToxiKind🤍")
st.sidebar.markdown("An AI-Based Toxicity Prediction Tool to Minimize Harm")

# Input 1 : Common name or IUPAC name
name_type = st.sidebar.selectbox(
    "Search by name type:",
    ["Common Name", "IUPAC Name"]
)

if name_type == "Common Name":
    names = df["title"].dropna().unique().tolist()
else:
    names = df["iupac_name"].dropna().unique().tolist()

name_input = st.sidebar.selectbox(f"Select a {name_type.lower()}:", sorted(names))

# Input 2: SMILES
smiles_input = st.sidebar.text_input("Or enter a SMILES string:")





# -------------------- Footer ----------------------
st.markdown("---")
st.caption("Built with 🤍 | for now, predicts Tox21 test set only")
