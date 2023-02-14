from fastapi import FastAPI

from src.auth.authentication_api import router_auth
from src.models.books import book_model
from src.models.books.book_api import router_book
from src.models.user import user_model
from src.database_connection import engine

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_book)

user_model.Base.metadata.create_all(bind=engine)
book_model.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "DATABASE CREATED"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
