import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.auth_service import auth
from db.create_tables import tables


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


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)
