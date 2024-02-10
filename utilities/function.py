from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import RetrievalQA
from langchain_community.tools import YouTubeSearchTool
from utilities.llms import llm_4, embeddings
import streamlit as st
import ast
from IPython.display import Image, display
import re
import ast


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
        llm=llm_4, 
        retriever=retriever,
        prompt=summary_template,
        verbose=True
        )
    result = dmac_qa.run(question)
    return str(result)

def cypher_qa(prompt):
    graph = Neo4jGraph(
    url="bolt://18.207.205.88:7687",
    username="neo4j",
    password="inclinations-odors-laser", 
    )

    CYPHER_GENERATION_TEMPLATE = """
    You are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
    Convert the user's question based on the schema.

    Use only the provided relationship types and properties in the schema.
    Do not use any other relationship types or properties that are not provided.

    Fine Tuning:

    For movie titles that begin with "The", move "the" to the end. For example "The 39 Steps" becomes "39 Steps, The" or "the matrix" becomes "Matrix, The".


    Schema:
    {schema}

    Question:
    {question}

    Cypher Query:
    """

    cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)
    
    cypher_chain = GraphCypherQAChain.from_llm(
        llm=llm_4,
        graph=graph,
        cypher_prompt=cypher_prompt,
        verbose=True
    )

    result = cypher_chain.run(prompt)
    return str(result)

def kg_qa(prompt):
    """
    Use the Neo4j Vector Search Index
    to augment the response from the LLM
    """
    neo4jvector = Neo4jVector.from_existing_index(
    embeddings,  
    url=st.secrets["NEO4J_URI"],  
    username=st.secrets["NEO4J_USERNAME"],  
    password=st.secrets["NEO4J_PASSWORD"],  
    index_name="moviePlots",  
    node_label="Movie",  
    text_node_property="plot", 
    embedding_node_property="plotEmbedding",  
    retrieval_query="""
    RETURN
        node.plot AS text,
        score,
        {
            title: node.title,
            directors: [ (person)-[:DIRECTED]->(node) | person.name ],
            actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
            tmdbId: node.tmdbId,
            source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
        } AS metadata
    """,
    )

    retriever = neo4jvector.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm_4,  
        chain_type="stuff",  
        retriever=retriever, 
    )
    # Handle the response
    result = qa.run(prompt)
    return str(result)

def youtube(prompt):
    youtube = YouTubeSearchTool()
    result = youtube.run(prompt)
    # Convert the string representation of the list back into a Python list
    result_list = ast.literal_eval(result)

    # Extract the first link
    first_link = result_list[0]
    
    # Example YouTube video URL
    video_url = first_link

    # Extract video ID from the URL
    video_id = re.search(r'(?<=v=)[^&#]+', video_url).group()

    # Construct the thumbnail URL
    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/0.jpg'

    # Display the thumbnail
    pic = display(Image(url=thumbnail_url))
    
    return f'{first_link}{pic}'