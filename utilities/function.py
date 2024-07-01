from utilities.llms import llm, embedding
from utilities.Prompt import ChatPrompt
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.tools import YouTubeSearchTool
import ast
import streamlit as st
import re
# Load environment variables from .env file
import os 
load_dotenv()

class chain_function():
    @staticmethod
    def gen_rag_answer(query:str)->str:
        # Load the FAISS index with allow_dangerous_deserialization set to True
        index_path = r"C:\Users\Ai Sukmoren\Desktop\chatbot\faiss_index"
        document_search = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
        
        # Perform a similarity search
        docs = document_search.similarity_search(query)

        # Load a QA chain
        chain = load_qa_chain(llm, chain_type="stuff")

        # Run the QA chain
        answer = chain.run(input_documents=docs, question=query)

        return answer
       
    @staticmethod
    def get_yotube_link(query):
        youtube = YouTubeSearchTool()
        result = youtube.run(query)
        # Convert the string representation of the list back into a Python list
        result_list = ast.literal_eval(result)

        # Extract the first link
        first_link = result_list[0]
        
        # Extract video ID from the URL
        video_id = re.search(r'(?<=v=)[^&#]+', first_link).group()

        # Construct the thumbnail URL
        thumbnail_url = f'https://img.youtube.com/vi/{video_id}/0.jpg'

        # Display the thumbnail using Streamlit
        st.image(thumbnail_url)

        # Use a markdown to display a clickable link with custom text
        display_text = "link"  # Custom text for the link

        template = PromptTemplate.from_template(
            """
            Yor task is to create a shot brief about a video user is looking for in excitment tone
            Instruction:
            - limit the word lenght to 50 words
        
            user prompt to find video on youtube: {ques}
        
            """
        )
        response = f"""
        here your url [{display_text}]({first_link}) !
        """
        return response