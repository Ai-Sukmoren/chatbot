from utilities.llms import llm, embedding
from utilities.Prompt import ChatPrompt
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
# Load environment variables from .env file
import os 
load_dotenv()

class chain_function():
    @staticmethod
    def gen_rag_answer(query:str)->str:
        # Load the FAISS index with allow_dangerous_deserialization set to True
        index_path = r"C:\Users\(Ai)AiSukmoren\Desktop\KMITL-present\faiss_index"
        document_search = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
        
        # Perform a similarity search
        docs = document_search.similarity_search(query)

        # Load a QA chain
        chain = load_qa_chain(llm, chain_type="stuff")

        # Run the QA chain
        answer = chain.run(input_documents=docs, question=query)

        return answer
    