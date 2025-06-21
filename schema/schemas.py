from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class UploadResponse(BaseModel):
    status: str
    columns: Optional[List[str]]
    message: Optional[str]

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    status: str
    result: Optional[Dict[str, Any]] = None     
    message: Optional[str] = None  