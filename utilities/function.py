from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.tools import YouTubeSearchTool
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from utilities.llms import llm_4
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
import pandas as pd
import os
import streamlit as st
import ast
import re
import ast

class func:

    @staticmethod
    def get_yotube_link(ques):
        youtube = YouTubeSearchTool()
        result = youtube.run(ques)
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
    
    @staticmethod
    def get_anime_data(ques:str):
        graph = Neo4jGraph(url=os.getenv('NE04J_CONN_URL'), 
                    username=os.getenv('NEO4J_USERNAME'), 
                    password=os.getenv('NEO4J_PASSWORD'),
                    database=os.getenv('NE04J_DB'))
        prompt = """
        You are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
        Convert the user's question based on the schema.

        instruction:
        - all animes is in lower cases

        Varibales:
        Schema {schema},
        Question {question}
        """

        cypher_generation_prompt = PromptTemplate(
            template=prompt,
            input_variables=["schema", "question"],
        )

        cypher_chain = GraphCypherQAChain.from_llm(
            llm=llm_4,
            graph=graph,
            cypher_prompt=cypher_generation_prompt,
            verbose=True
        )
        res = cypher_chain.invoke(ques)
        res = res['result']
        return res