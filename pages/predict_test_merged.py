import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_searchbox import st_searchbox
import requests
from frontendlogic.llm import toxikind_summarizer


# -------------------- TOX21 ASSAY DEFINITIONS --------------------
TOX21_ASSAYS = [
    "Androgen Receptor (NR-AR)",
    "Androgen Receptor LBD (NR-AR-LBD)",
    "Aryl Hydrocarbon (NR-AhR)",
    "Estrogen Receptor (NR-ER)",
    "Estrogen Receptor LBD (NR-ER-LBD)",
    "PPAR-gamma (NR-PPARγ)",
    "Antioxidant Response (SR-ARE)",
    "DNA Damage (SR-ATAD5)",
    "Heat Shock Response (SR-HSE)",
    "Mitochondrial Membrane (SR-MMP)",
    "p53 Stress Response (SR-p53)",
    "Aromatase Inhibition (NR-Arom)"
]

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    return pd.read_pickle('media/compounds.pkl')

df = load_data()
smiles_list = df["smiles"].dropna().unique().tolist()

def search_smiles(term: str):
    term = term.strip().upper()
    return [s for s in smiles_list if term in s.upper()]

# -------------------- UI HEADER --------------------
st.markdown(
    """
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style="font-size: 4rem; font-weight: 700; color: #006d77; margin-bottom: 0.2em;">
            ToxiKind 🤍
        </h1>
        <p style="font-size: 1.2rem; font-weight: 400; color: #595959; margin-top: 0;">
            An AI-Based Toxicity Prediction Tool to Minimize Harm
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- INPUT SECTION --------------------
st.header("Compound Input")

col1, col2 = st.columns([1, 3])

with col1:
    search_mode = st.radio("Search by:", ["Name", "SMILES"], index=0)

name_input = None
smiles_input = None

with col2:
    if search_mode == "Name":
        name_type = st.selectbox("Name type:", ["Common Name", "IUPAC Name"])
        names = df["title"].dropna().unique().tolist() if name_type == "Common Name" else df["iupac_name"].dropna().unique().tolist()
        name_input = st.selectbox(f"Select a {name_type.lower()}:", ["🔍 Select a compound..."] + sorted(names))
    else:
        smiles_input = st_searchbox(search_smiles, key="smiles_searchbox", placeholder="Press C and select a SMILES string...")

input_ready = (
    (smiles_input is not None and smiles_input != "")
    if search_mode == "SMILES"
    else name_input not in ["", "🔍 Select a compound..."]
)

predict_button = st.button("Predict Toxicity", disabled=not input_ready, type="primary", use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

# -------------------- PREDICTION --------------------
if predict_button:
    compound_id = None

    if search_mode == "Name":
        if name_input:
            match = df[df["title"] == name_input] if name_type == "Common Name" else df[df["iupac_name"] == name_input]
    else:
        match = df[df["smiles"] == smiles_input]

    if not match.empty:
        compound_id = match.iloc[0]["ID"]

        with st.spinner("🧪 Predicting toxicity..."):
            try:
                data = {
                    "compound": compound_id,
                }
                response = requests.get("http://localhost:8000/predict/", params=data)
                if response.status_code != 200:
                    st.error(f"Prediction failed with status code {response.status_code}")
                    st.stop()

                st.write(pd.DataFrame(response.json()))

            except Exception as e:
                st.error(f"Cannot connect to server: {e}")
                st.stop()

        results = response.json()
        st.success("✅ Prediction completed!")
        st.subheader("🧪 Toxicity Results")

        predictions = []
        probabilities = []
        acronyms = []

        for assay in TOX21_ASSAYS:
            tox21_id = assay.split("(")[-1].replace(")", "")
            acronyms.append(tox21_id)
            predictions.append(results.get(f"{tox21_id}_prediction", "N/A"))
            probabilities.append(results.get(f"{tox21_id}_probability", 0))

        results_df = pd.DataFrame({
            "Assay": TOX21_ASSAYS,
            "Toxic?": ["Yes" if p == 1 else "No" for p in predictions],
            "Probability": [f"{p:.2%}" for p in probabilities]
        })

        st.dataframe(results_df, use_container_width=True)

        # -------------------- RADAR CHART --------------------
        st.subheader("📊 Overview of Probabilities")

        values = probabilities.copy()
        angles = np.linspace(0, 2 * np.pi, len(acronyms), endpoint=False).tolist()

        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color='crimson', linewidth=2)
        ax.fill(angles, values, color='crimson', alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(acronyms, fontsize=9, color='black')
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"], fontsize=8)
        ax.set_ylim(0, 1)
        ax.grid(True, linestyle='dotted', alpha=0.6)

        st.pyplot(fig)

        # -------------------- LLM SUMMARY --------------------
        st.subheader("🤖 Summary (LLM Interpretation)")

        try:
            # toxikind_summarizer accepts a dictionary
            chain = toxikind_summarizer(results_df=results)
            summary = chain.run(results_df=results)
            st.write(summary)
        except Exception as e:
            st.warning(f"LLM summary failed: {e}")


    else:
        st.warning("Please provide a valid input.")
