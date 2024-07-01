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
            8. any question about description or long explaination use `text` property in Content node
            9. Always return `newsID` property everytime you get answer from `text` property in Content node
            10. Always put osVersion 10.0.22631.3737 in the list
            
            Schema:
            {schema}
            
            Samples:
            use input: list me a laptop name that match this build-number
            query sample:
            ```
            MATCH (n:Laptop)
            WHERE n.osVersion IN ['6.3.9600.21503', '6.2.9200.24414', '6.1.7601.26664', '6.0.6003.22216', '10.0.14393.6167', '10.0.10240.20107', '10.0.19045.3324', '10.0.22621.2134', '10.0.19044.3324', 
            '10.0.22000.2295', '10.0.20348.1906', '10.0.20348.1903', '10.0.17763.4737','10.0.22631.3737']
            RETURN n.name 
            ```
            
            Question: {question}
            """

        CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE)
        return CYPHER_GENERATION_PROMPT
    
    
    