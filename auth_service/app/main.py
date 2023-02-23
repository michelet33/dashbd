import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from db.create_tables import tables
from db.database import SessionLocal
from api.v1.services import auth

app = FastAPI()
# origins = [
#     "http://localhost:5051/",
# ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv('.env')


app = FastAPI()

# TODO to avoid csrftokenError

app.include_router(auth)
app.include_router(tables)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.129", port=5000)
