from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import Header, APIRouter
from ..utils import auth_required

report = APIRouter()

@report.get("/info/")
@auth_required
def get_information(
) -> JSONResponse:
    return JSONResponse(content={"info": "The answer is 42."})
