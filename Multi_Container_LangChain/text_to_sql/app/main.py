from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import logging
import os
from sql_generator import generate_sql
from dotenv import load_dotenv
import uvicorn 

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title ="Text-to-SQL API",description = "Converts Natural Language to SQL Queries.")

class QueryInput(BaseModel):
    query:str

class SQLResponse(BaseModel):
    sql_query:str

@app.post("/generate",response_model=SQLResponse)
async def generate_sql_query(input:QueryInput):
    try:
        sql_query = generate_sql(input.query)
        logger.info(f"Query {input.query}, SQL: {sql_query}")
        return {"SQL": sql_query}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code = 500 , detail=str(e))
    

@app.get("/health")
async def health_check():
    return {"status":"healthy"}    

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port = 8002)
