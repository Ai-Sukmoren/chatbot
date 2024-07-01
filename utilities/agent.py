from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from utilities.llms import llm
from utilities.function import chain_function


gen_rag_answer = """This tool is use to answer the question based on the information in vector index or rag only"""

tools = [
    Tool.from_function(
        name="gen_rag_answer",
        description=gen_rag_answer,
        func=chain_function.gen_rag_answer,
        return_direct=True,
    )
]

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=1,
    return_messages=True,
)

agent_prompt = PromptTemplate.from_template(
    """
    ROLES:
    My name is 'Jarvis.'
    I am an AI assistant specialized in educational technology and AI applications in education.
    My aim is to provide comprehensive and precise information on AI and its role in education.
    What I can do:
    - Generally answering about anything that user ask.
    - Answer questions about AI in education, including applications, best practices, and innovative tools.
    - Answer the question in vector database using RAG technique.

    TOOLS:
    ------

    You have access to the following tools:

    {tools}

    To use a tool, please use the following format:

    ```
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ```
    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

    ```
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]
    ```

    Begin!

    Previous conversation history:
    {chat_history}

    New input: {input}
    {agent_scratchpad}
      
        """)

agent = create_react_agent(llm, 
                           tools, 
                           agent_prompt)

agent_executor = AgentExecutor(agent=agent, 
                               tools=tools, 
                               memory=memory, 
                               verbose=True,
                               handle_parsing_errors=True)

def generate_response(prompt):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = agent_executor.invoke({"input": prompt})
    response = response['output']
    # Replace '\n```' with an empty string
    response = response.replace('\n```', '')

    # Replace 'None' with a single space ' '
    response = response.replace('None', ' ')
    return response