import streamlit as st
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from utilities.function import youtube_streamlit

# Streamlit and OpenAI API key handling
if "llm_initialization_state_flag" not in st.session_state:
    st.session_state.llm_initialization_state_flag = False

if 'api_key' not in st.session_state:
    with st.sidebar:
        st.info("""
                You need to input your OpenAI API key to use the chatbot. This chatbot utilizes OpenAI GPT model.
                """)
        api_key = st.text_input('Input your OpenAI API key', type='password', key='api_key')
else:
    api_key = st.session_state.api_key

llm_4 = None
# Initialize llm model if API key is provided
if api_key:
    llm_4 = ChatOpenAI(
        temperature=0,
        model="gpt-4-1106-preview",
        openai_api_key=api_key)
    st.session_state.llm_initialization_state_flag = True
else:
    st.info("Please input your OpenAI API key to use the chatbot")
    # Exit the script early if no API key is provided to avoid errors
    raise SystemExit("API key not provided")

# Assuming the rest of your code relies on llm_4 being correctly initialized
# Define tools and agent logic after llm_4 is initialized
tools = [
    Tool.from_function(
        name="General Chat",
        description="For general chat not covered by other tools",
        func=llm_4.invoke,
        return_direct=True
    ),
    Tool.from_function(
        name="Youtube search",
        description="For proving youtube url to user",
        func=youtube_streamlit,
        return_direct=True,
    )     
]

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=3,
    return_messages=True,
)

agent_prompt = PromptTemplate.from_template(
    """
        You general chat assistant helper
        Be as helpful as possible and return as much information as possible.

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

agent = create_react_agent(llm_4, tools, agent_prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

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