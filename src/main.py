from fastapi import FastAPI

from src.auth.router import router as router_auth
from src.database_connection import engine, Base
from src.models.user.router import router as router_user
from src.models.books.book_api import router_book
from src.models.test_topic.topic_api import router_topic
from src.models.lessons.lesson_api import router_lessons
from src.models.test_level.level_api import router_level_test
from src.models.media_file.media_api import router_media



app = FastAPI()

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_book)
app.include_router(router_topic)
app.include_router(router_lessons)
app.include_router(router_level_test)
app.include_router(router_media)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "DATABASE CREATED"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
