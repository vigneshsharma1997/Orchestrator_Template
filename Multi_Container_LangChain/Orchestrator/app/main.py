from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from orchestrator import route_query
import logging
import os
from dotenv import load_dotenv
import uvicorn 

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title ="Orchestrator API",description = "Routes Queries to RAG or Text-to-Sql services.")

class QueryInput(BaseModel):
    query:str

class QueryResponse(BaseModel):
    result:str
    service:str

@app.post("/process",response_model=QueryResponse)
async def process_query(input:QueryInput):
    try:
        result , service = await route_query(input.query)
        logger.info(f"Query {input.query}, routed to : {service}")
        return {"result": result, "service":service}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code = 500 , detail=str(e))
    
@app.get("/health")
async def health_check():
    return {"status":"healthy"}

# if __name__ == "__main__":
#     uvicorn.run(app,host="0.0.0.0",port = 5000)
