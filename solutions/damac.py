from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from solutions.llm import llm, embeddings
from langchain.prompts import PromptTemplate


def dmac_qa(question):
    """
    Use the  Vector Search Index
    to augment the response from the LLM
    """
    embedding = embeddings

    damac_vectorstore = FAISS.load_local("damac_database", embedding)

    template = """
    You are an expert female lawyer who is specialized in ansewering various ploblem regard to the agreement between 2 parties.

    If no data is returned, do not attempt to answer the question.
    Do not include any explanations or apologies in your responses. 


    Question: {question}
    context: {context}
    """

    summary_template = PromptTemplate(input_variables=['question','context'],template= template)
    
    retriever = damac_vectorstore.as_retriever()
    dmac_qa = RetrievalQA.from_llm(
        llm=llm, 
        retriever=retriever,
        prompt=summary_template,
        verbose=True
        )
    result = dmac_qa.run(question)
    return str(result)