import httpx
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
load_dotenv()
groq_api = os.getenv("groq_api_key")

def generate_sql(query):
    llm = ChatGroq(model = "Gemma2-9b-It",groq_api_key=groq_api)
    prompt = ChatPromptTemplate.from_template(
        "Convert the following natural language query to SQL for a database with tables :"
        "users (id,name,email) , orders (id,user_id,amount,date). "
        "Query: {query}\nSQL:"
    )
    parser = StrOutputParser()
    chain = prompt|llm|parser
    sql_query = chain.invoke({"query":query})
    return sql_query