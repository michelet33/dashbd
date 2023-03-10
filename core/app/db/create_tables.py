from .models import tags, users, logs, chargers, params
from fastapi import APIRouter
from .database import engine


tags.Base.metadata.create_all(bind=engine)
users.Base.metadata.create_all(bind=engine)
logs.Base.metadata.create_all(bind=engine)
chargers.Base.metadata.create_all(bind=engine)
params.Base.metadata.create_all(bind=engine)

tables = APIRouter()


@tables.get("/tables/create/")
def create_tables():
	print("create_tables")
