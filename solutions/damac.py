
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from solutions.llm import llm


def dmac_qa(prompt):
    """
    Use the  Vector Search Index
    to augment the response from the LLM
    """
    embeddings = OpenAIEmbeddings()

    damac_vectorstore = FAISS.load_local("damac_database", embeddings)


    retriever = damac_vectorstore.as_retriever()
    dmac_qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever,
    verbose=True
    )
    result = dmac_qa.run(prompt)
    return str(result)