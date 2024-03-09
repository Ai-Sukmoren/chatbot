from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import RetrievalQA
from langchain_community.tools import YouTubeSearchTool
from langchain_experimental.agents.agent_toolkits import create_csv_agent,create_pandas_dataframe_agent,create_python_agent
from langchain.agents import AgentType, initialize_agent, Tool
from utilities.llms import llm_4,llm_3 , embeddings
from langchain_experimental.tools import PythonREPLTool
import pandas as pd
import os
import streamlit as st
import ast
import re
import ast

class func:

    @staticmethod
    def get_yotube_link(prompt):
        youtube = YouTubeSearchTool()
        result = youtube.run(prompt)
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
        
            user prompt to find video on youtube: {prompt}
        
            """
        )
        #llm_3 to descibe the video
        llm_chain = LLMChain(
            llm=llm_3,
            prompt=template,
            verbose=True
        )

        input_variables = {"prompt": prompt}

        res = llm_chain.invoke(input_variables)
        res = str(res['text'])

        response = f"""
        here your url [{display_text}]({first_link}) !\n
        {res}
        """
        return response

    @staticmethod
    def get_pandas_graph(prompt,df=False):
        if df == False:
            df = input("please insert your dataframe")
        else:
            pandas_agent = create_pandas_dataframe_agent(
            llm=llm_4,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            df = df,
            verbose=False,
            handle_parsing_errors=True,)


            prompt = "plot a  graph for me, I want female to be pink and male to be blue and tell me a little about dataframe"

            result = pandas_agent.invoke({"input":prompt})

            pandas_agent.invoke(result["output"])