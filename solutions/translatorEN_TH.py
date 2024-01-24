from langchain.chains import  LLMChain
from langchain import PromptTemplate
from langchain.prompts import PromptTemplate
from solutions.llm import llm_3


#assign variables
input_language = 'EN'
output_language = 'TH'

#promptTemplate
summary_templates = """
   You are a translation specialist with 35 years of experience in translating from {input_language} to {output_language}. Given the question {Question}, 
   your task is to translate it into {output_language}. If the question is already in {output_language}, check for any grammatical mistakes and correct them if necessary.
    Caution:
    Provide only the answer, without any explanations.
    """

summary_prompts_template = PromptTemplate(input_variables=['Question','input_language','output_language'], template = summary_templates)

chain = LLMChain(llm=llm_3
                 
                 , prompt=summary_prompts_template) 

def translate_qa_en_th(prompt):
    Answer = chain.run(Question=prompt,input_language=input_language,output_language=output_language)
    return str(Answer) 
