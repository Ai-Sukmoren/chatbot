from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from utilities.llms import llm_4
from utilities.function import youtube_streamlit



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