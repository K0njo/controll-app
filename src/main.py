from fastapi import FastAPI

from src.auth.authentication_api import router_auth
from src.database_connection import engine, Base
from src.models.media_file.media_api import router_media


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_media)



Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "DATABASE CREATED"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
