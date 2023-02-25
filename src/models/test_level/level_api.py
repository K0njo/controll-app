import random

from fastapi import APIRouter, HTTPException, Depends
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from src.database_connection import get_db
from src.models.test_level.level_model import Level
from src.models.test_level.level_schema import LevelSchema

router_level_test = APIRouter(prefix="/level-test", tags=['level test'])


@router_level_test.get("/question/")
def get_book(question: int, db: Session = Depends(get_db)):
    one_question = db.query(Level).filter(Level.id == question).first()
    if not one_question:
        raise HTTPException(status_code=404, detail="Question not found")
    response = {
        "question": one_question.question,
        "media_file_id": one_question.media_file_id,
        "answers": list(one_question.answer.values())
    }

    random.shuffle(response["answers"])

    response["answers"] = {key: response["answers"].pop() for key in sorted(one_question.answer.keys())}

    return response


@router_level_test.get("/qwestion/result")
def tesult_test():
    pass


@router_level_test.post("/add-qwestion/")
def post_book(qwestion_add: LevelSchema, db: Session = Depends(get_db)):
    new_qwestion = Level(section_name=qwestion_add.section_name,
                    question=qwestion_add.question,
                    answer=qwestion_add.answer)

    try:
        db.add(new_qwestion)
        db.commit()
        db.refresh(new_qwestion)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Question already exists")

    return {"message": "Created question"}


@router_level_test.post("/qwestion/answer-user/")
def answer_user():
    pass



@router_level_test.patch("/update-book/{book_id}")
def update_book(id: int, qwestion: LevelSchema, db: Session = Depends(get_db)):
    up_question = db.query(Level).filter(Level.id == id).first()
    if not up_question:
        raise HTTPException(status_code=404, detail="Question not found")
    up_question.section_name = qwestion.section_name
    up_question.question = qwestion.question
    up_question.answer = qwestion.answer
    db.commit()
    return {"message": "Question updated"}


@router_level_test.delete("/delete-question/{question_id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    del_question = db.query(Level).filter(Level.id == id).first()
    if not del_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(del_question)
    db.commit()
    return {"message": "Question deleted"}
