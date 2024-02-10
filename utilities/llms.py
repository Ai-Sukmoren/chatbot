import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings


# Load environment variables from .env file
load_dotenv()

AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")


llm_4 = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_version="2023-03-15-preview",
    azure_deployment="gpt4_1106",
    openai_api_key=AZURE_OPENAI_API_KEY,
)

llm_3 = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_version="2023-03-15-preview",
    azure_deployment="gpt-35-turbo-0613",
    openai_api_key=AZURE_OPENAI_API_KEY,
)

embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            openai_api_version="2023-03-15-preview",
            deployment="embedada",
            openai_api_key=AZURE_OPENAI_API_KEY,
            )
