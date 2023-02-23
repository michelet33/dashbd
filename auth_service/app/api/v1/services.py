from typing import Optional
from fastapi import Response, Depends, Body
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from fastapi import Header, APIRouter
from sqlalchemy.orm import Session
from db.models.logs import Logs
from db.database import get_db

auth= APIRouter()

@auth.post("/login/")
def login(
        authorization: Optional[str] = Header(None)
) -> Response:
    if not authorization == "michele":
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    return Response(status_code=HTTP_200_OK)

@auth.post("/log/add/")
def add_log(d= Body(), db: Session = Depends(get_db)):
    print(d)
    if len(d)>0:
        db_log = Logs(charger_id=d['charger_id'], action=d['action'], content=d['content'])
        db.add(db_log)
        db.commit()
        # db.refresh(db_log)
