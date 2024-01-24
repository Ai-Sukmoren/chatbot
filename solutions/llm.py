import streamlit as st
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model=st.secrets["OPENAI_MODEL_4"],
    temperature=0
)


llm_3 = ChatOpenAI(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model=st.secrets["OPENAI_MODEL_3"],
    temperature=0
)


from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])

