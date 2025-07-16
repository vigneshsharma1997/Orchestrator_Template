import httpx
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
load_dotenv()
groq_api = os.getenv("groq_api_key")
print(groq_api)
async def route_query(query):
    llm = ChatGroq(model = "Gemma2-9b-It",groq_api_key=groq_api)
    print("Inside Route Query")
    prompt = ChatPromptTemplate.from_template(
        "Determine if the query is asking for general information RAG or a Database Query SQL."
        "Return 'RAG' or 'SQL' . Query :{query}"
    )
    parser = StrOutputParser()
    chain = prompt|llm|parser

    intent = chain.invoke({"query":query})
    print("Intent : ",intent)

    async with httpx.AsyncClient() as client:
        if intent.content.strip() == "SQL":
            response = await client.post(
                f"{os.getenv('TEXT_TO_SQL_URL')}/generate",
                json = {"query":query}
            )
            response.raise_for_status()
            return response.json()["sql_query"] , "text_to_sql"
        else:
            response = await client.post(
                f"{os.getenv("RAG_URL")}/ask",
                json = {"question":query}
            )
            response.raise_for_status()
            return response.json()["answer"], "rag_chatbot"

