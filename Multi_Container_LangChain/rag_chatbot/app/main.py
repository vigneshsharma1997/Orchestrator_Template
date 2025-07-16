from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
# from orchestrator import route_query
import logging
import os
from dotenv import load_dotenv
import uvicorn 
from typing import List
# from rag_utils import initialize_rag_chain,query_chain
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title ="RAG Chatbot API",description = "API for Retrieval Augmented Generation.")

# rag_chain = initialize_rag_chain()

class QueryInput(BaseModel):
    question:str

class QueryResponse(BaseModel):
    answer : str
    sources: List[str]


@app.post("/ask",response_model = QueryResponse)
async def ask_question(query:QueryInput):
    try:
        # response , sources = query_chain(rag_chain,query.question)
        response = "RAG"
        sources = ["Document1.txt"]
        logger.info(f"Question : {query.question} , answer : {response}")
        return {"answer":response,"sources":sources}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code = 500 , detail=str(e))
    
@app.get("/health")
async def health_check():
    return {"status":"healthy"}

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port = 8001)

# uvicorn main:app --host localhost --port 8001
