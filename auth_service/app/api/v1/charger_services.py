# from typing import Optional
import datetime
import json
# import jsonify as jsonify
from fastapi import Depends, Body, Response
from fastapi.responses import JSONResponse
# from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from fastapi import Header, APIRouter
from sqlalchemy.orm import Session
from db.models.chargers import Chargers
from db.models.params import Params
from db.database import get_db

charger= APIRouter()

@charger.get("/ocpp/requests/get/")
async def get_all_request_ocpp(db: Session = Depends(get_db)):
    """
    :type db: object
    """
    obj = db.query(Params).filter(Params.valid == True, Params.id_tags == 1).order_by(Params.order)
    d = []
    for o in obj:
        d.append((dict((name, str(getattr(o, name))) for name in vars(o) if not name.startswith('_'))))
    # print(d)
    return d

@charger.get("/chargers/get/")
async def get_all_chargers(db: Session = Depends(get_db)):
    """
    :type db: object
    """
    obj =  db.query(Chargers).filter(Chargers.valid == True)
    d = []
    for o in obj:
        d.append((dict((name, str(getattr(o, name))) for name in vars(o) if not name.startswith('_'))))
    return d

@charger.post("/charger/set/")
def add_log(d= Body(), db: Session = Depends(get_db)):
    # print(d)
    if len(d)>0:
        c = db.query(Chargers).filter(Chargers.charger_id == d['charger_id']).first()
        if not c:
            db_charger = Chargers(charger_id=d['charger_id'],
                                  charge_point_model=d['charge_point_model'],
                                  charge_point_vendor=d['charge_point_vendor'])
            db.add(db_charger)
            db.commit()
        else:
            c.valid = True
            c.updated_at = datetime.datetime.now()
            db.commit()

@charger.post("/chargers/invalid/")
def invalid_all_chargers(db: Session = Depends(get_db)):
    chargers = db.query(Chargers).filter(Chargers.valid == 1)
    if chargers:
        for c in chargers:
            print(c)
            # c.valid = False
            # c.updated_at = datetime.datetime.now()
            # db.commit()

# def get_charger(charger_id, db: Session = Depends(get_db)) -> Chargers:
#     return db.query(Chargers).filter(Chargers.charger_id == charger_id).first()
