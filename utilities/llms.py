from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
# Load environment variables from .env file
import os
load_dotenv()

# Access the environment variables
API_KEY = os.getenv('api_key')

llm = ChatOpenAI(
    api_key=API_KEY,
    model='gpt-4o', 
)

embedding = OpenAIEmbeddings(
    api_key=API_KEY,
    model='text-embedding-3-small'
)