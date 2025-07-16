import httpx
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassThrough 
load_dotenv()
groq_api = os.getenv("groq_api_key")


def initialize_rag_chain():
    embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    llm = ChatGroq(model = "Gemma2-9b-It",groq_api_key=groq_api)
    vector_store = Chroma(persist_directory = "/app/chroma_db",embedding_functions=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k":3})
    prompt = ChatPromptTemplate.from_template("Answer the question based on the context : {context}\n Question : {question} \n Answer:")
    chain = (
        {"context":retriever,"question":RunnablePassThrough}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def query_chain(chain,question):
    response = chain.invoke(question)
    sources = ["documents1.txt","documents2.txt"]
    return response,sources