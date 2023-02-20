from typing import Optional
from fastapi import Response
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from fastapi import Header, APIRouter

auth = APIRouter()


@auth.post("/login/")
def login(
        authorization: Optional[str] = Header(None)
) -> Response:
    if not authorization == "michele":
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    return Response(status_code=HTTP_200_OK)
