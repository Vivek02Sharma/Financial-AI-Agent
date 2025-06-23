from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

from schema.schemas import UploadResponse, QueryRequest, QueryResponse 
from utils.read_file import file_to_dataframe
from agent.financial_agent import query_financial_data

app = FastAPI()

df_store = {"df": None} # lets make in-memory storage

@app.get("/")
def home():
    return JSONResponse(
        status_code = 200,
        content = {"message": "This is Finalcial AI Agent."}
    )

@app.post("/upload", response_model = UploadResponse)
async def user_input(file: UploadFile = File(..., description = "Upload csv or excel file")):
    try:
        df = file_to_dataframe(file)
        df_store["df"] = df
        return UploadResponse(
            status = "success",
            columns = list(df.columns), message = None
        )
    except Exception as e:
        return UploadResponse(
            status = "error",
            columns = None,
            message = str(e)
        )

@app.post("/query", response_model = QueryResponse)
async def user_query(request: QueryRequest):
    df = df_store.get("df")
    # print(df)
    if df is None:
        return QueryResponse(
            status = "error",
            result = None,
            message = "No file uploaded."
        )
    
    result = await query_financial_data(request.prompt, df)
    # print(result)
    if isinstance(result, dict) and "error" in result:
        return QueryResponse(
            status = "error",
            result = None,
            message = result["error"]
        )
    
    return QueryResponse(
        status = "success",
        result = {"response": result},
        message = "Query executed successfully."
    )