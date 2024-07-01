import streamlit as st
import pandas as pd
from utilities.agent import generate_response
from utilities.llms import embedding
from time import sleep
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os

def write_message(role, content, save=True):
    """This is a helper function that saves a message to the session state and then writes a message to the UI."""
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    if role == "assistant":
        with st.chat_message(role, avatar="🔒"):
            st.markdown(content)
    else:
        with st.chat_message(role, avatar="👤"):
            st.markdown(content)

def handle_submit(message):
    with st.spinner('Analyzing your document...'):
        response = generate_response(message)
        sleep(1)
        write_message('assistant', response)

def process_pdf_to_faiss_search(pdf_path, embedding_model):
    # Read the PDF file
    pdf = PdfReader(pdf_path)
    
    # Extract text from the PDF
    raw_text = ''
    for page in pdf.pages:
        content = page.extract_text()
        if content:
            raw_text += content
    
    # Split the text using Character Text Splitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)
    
    # Create FAISS document search
    document_search = FAISS.from_texts(texts, embedding_model)
    
    return document_search

def handle_pdf_upload(pdf_file):
    if pdf_file:
        # Ensure the temporary directory exists
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Save the uploaded PDF to a temporary location
        temp_pdf_path = os.path.join(temp_dir, pdf_file.name)
        with open(temp_pdf_path, "wb") as f:
            f.write(pdf_file.read())

        # Process the PDF and create the FAISS document search
        embedding_model = embedding
        document_search = process_pdf_to_faiss_search(temp_pdf_path, embedding_model)
        
        # Provide feedback to the user
        st.write("""
                 PDF processed and vector store created successfully\n 
                 !caution\n
                 delete the file before proceed with the question 
                 """)
        
        # (Optional) Save the FAISS index to a file if needed      
        document_search.save_local("faiss_index")

if __name__ == '__main__':
    st.set_page_config(page_title='School Demo Session using AI', page_icon='📚', layout='centered')

    # Use columns to place the logo on the left.
    col1, col2, col3 = st.columns([1, 3, 1])  # Center column is much wider to keep the logo on the left.
    with col1:
        st.image(r"C:\Users\Ai Sukmoren\Desktop\kmitl-chatbot\pic\Logo Iambest2021-13.png", width=120)  # Adjust the path as needed

    with st.container():
        st.title("School Demo Session using AI 📚")
        st.markdown("""
        Welcome to the School Demo Session using AI

        You can ask me about:
        - AI applications in education
        - How AI can assist in learning and teaching

        **This chatbot is designed to assist you with various AI-related questions and provide insights.**
        """)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm here to help you with AI-related queries in education. How can I assist you today?"}]

    for message in st.session_state.messages:
        write_message(message['role'], message['content'], save=False)

    # File uploader for PDF files
    uploaded_pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_pdf_file is not None:
        handle_pdf_upload(uploaded_pdf_file)

    if prompt := st.chat_input("Ask me about AI applications in education or any related inquiries."):
        write_message('user', prompt)
        handle_submit(prompt)
