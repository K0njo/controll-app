from fastapi import FastAPI

from src.auth.authentication_api import router_auth
from src.database_connection import engine, Base
from src.models.books.book_api import router_book

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_book)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "DATABASE CREATED"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
