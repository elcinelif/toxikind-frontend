# -------------------- LANGCHAIN IMPORTS--------------------
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import streamlit as st


def toxikind_summarizer(results_df):
    print(st.secrets.key)
    api_key = st.secrets.key
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2, google_api_key=api_key)

    template = """
    You are a scientific assistant of an ML tool aiming to predict toxicities of given compounds.
    The ML tool was trained with Tox21 training set.
    Given the following assay results for toxicity prediction of the compound,
    summarize the likely biological impacts of the compound in human-friendly language.

    Assay results:
    {results_df}

    Summarize in clear, non-technical terms:
    """

    prompt = ChatPromptTemplate.from_template(template)
    return LLMChain(llm=model, prompt=prompt)
