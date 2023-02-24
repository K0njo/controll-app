from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from src.auth.authentication_api import get_db
from src.models.lessons.lesson_schema import LessonSchema
from src.models.lessons import lesson_model as model
from src.models.lessons.lesson_model import Lesson

router_lessons = APIRouter(prefix="/lessons", tags=["lessons"])

@router_lessons.get("/all-lessons/")
def get_all_lessons(page: int = 1, page_size: int = 5, db: Session = Depends(get_db)):
    skip = (page-1) * page_size
    all_lessons = db.query(Lesson).offset(skip).limit(page_size).all()

    return all_lessons

@router_lessons.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: int, db:Session = Depends(get_db)):

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException (status_code= 404, detail="Lesson doesn't exist")

    return lesson


@router_lessons.post("/add-lesson/")
def add_lesson(new_lesson: LessonSchema, db: Session = Depends(get_db)):
    create_lesson_model = model.Lesson()

    create_lesson_model.level = new_lesson.level
    create_lesson_model.topic_name = new_lesson.topic_name
    create_lesson_model.topic_description = new_lesson.topic_description


    try:
        db.add(create_lesson_model)
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code= 400, detail="Lesson already exists")

    return "Lesson has been created"


@router_lessons.patch("/update-lesson/{lesson_id}")
def update_lesson(lesson_id: int, lesson: LessonSchema, db: Session = Depends(get_db)):
    update_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if not update_lesson:
        raise HTTPException(status_code=404, detail="Lesson doesn't exist")

    update_lesson.level = lesson.level
    update_lesson.topic_name = lesson.topic_name
    update_lesson.topic_description = lesson.topic_description

    db.commit()

    return "Lesson has been updated"


@router_lessons.delete("/delete-lesson/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException (status_code= 404, detail="Lesson doesn't exists")

    db.delete(lesson)
    db.commit()

    return "Lesson has been deleted"
