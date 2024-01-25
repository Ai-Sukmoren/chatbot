from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from solutions.llm import llm
from solutions.damac import dmac_qa
from solutions.youtube import youtube
from solutions.graph import cypher_qa
from solutions.plot import kg_qa
from solutions.translatorEN_TH import translate_qa_en_th
from solutions.translatorTH_EN import translate_qa_th_en

tools = [
    Tool.from_function(
        name="General Chat",
        description="For general chat not covered by other tools",
        func=llm.invoke,
        return_direct=True,
    ),
    Tool.from_function(
        name="Damac agreement",
        description="Provides information about DAMAC agreement",
        func=dmac_qa,
        return_direct=True,
    ),
    Tool.from_function(
        name="Youtube search",
        description="For proving youtube url to user",
        func=youtube.run,
        return_direct=True,
    ),
    # Tool.from_function(
    #     name="Cypher QA",
    #     description="Provide information about movies questions using Cypher",
    #     func=cypher_qa,
    #     return_direct=True,
    # ),
    # Tool.from_function(
    #     name="Vector Search Index",
    #     description="Provides information about movie plots using Vector Search",
    #     func=kg_qa,
    #     return_direct=True,
    # ),
        Tool.from_function(
        name="Translator from TH to EN",
        description="use when need to translate thai to english",
        func=translate_qa_th_en,
        return_direct=True,
    ),
        Tool.from_function(
        name="Translator from EN to TH",
        description="use when need to transalte english to thai",
        func=translate_qa_en_th,
        return_direct=True,
    ),
        
]

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True,
)

agent_prompt = PromptTemplate.from_template(
    """
        You are a lawyer who is specilized in answering ansewer regard to law and regulation decision question.
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
        """
)
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)




def generate_response(prompt):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = agent_executor.invoke({"input": prompt})

    return response['output']

