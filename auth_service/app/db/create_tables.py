from .models import tags, users
from fastapi import APIRouter
from .database import engine


tags.Base.metadata.create_all(bind=engine)
users.Base.metadata.create_all(bind=engine)

tables = APIRouter()


@tables.get("/tables/create/")
def create_tables():
	print("create_tables")
