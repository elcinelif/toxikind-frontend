# -------------------- Imports ----------------------
import streamlit as st
# -------------------- Header ----------------------

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
