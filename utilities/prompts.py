from langchain.prompts import PromptTemplate

class ChatPrompt():

    @staticmethod
    def prompt_cypher_query() -> PromptTemplate:        
        CYPHER_GENERATION_TEMPLATE = """
        You are an expert Neo4j Cypher translator who understands the question in english and convert to Cypher strictly based on the Neo4j Schema provided and following the instructions below:
            1. Generate Cypher query compatible ONLY for Neo4j Version 5
            2. Do not use EXISTS, SIZE keywords in the cypher. Use alias when using the WITH keyword
            3. Use only Nodes and relationships mentioned in the schema
            4. Always enclose the Cypher output inside 3 backticks
            5. Always do a case-insensitive and fuzzy search for any properties related search. Eg: to search for a Team name use `toLower(t.name) contains 'neo4j'`
            6. Always use aliases to refer the node in the query
            7. Cypher is NOT SQL. So, do not mix and match the syntaxes

            Schema:{schema}
            Question: {question}
            """

        CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE)
        return CYPHER_GENERATION_PROMPT