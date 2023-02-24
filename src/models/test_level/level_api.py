from fastapi import APIRouter, HTTPException, Depends
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from src.database_connection import get_db
from src.models.test_level.level_model import Level
from src.models.test_level.level_schema import LevelSchema

router_level_test = APIRouter(prefix="/level-test", tags=['level test'])


@router_level_test.get("/qwestion/")
def get_book(qwestion: int, db: Session = Depends(get_db)):
    one_qwestion = db.query(Level).filter(Level.id == qwestion).first()
    if not one_qwestion:
        raise HTTPException(status_code=404, detail="Qwestion not found")
    return one_qwestion


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
        raise HTTPException(status_code=400, detail="Qwestion already exists")

    return {"message": "Created qwestion"}


@router_level_test.patch("/update-book/{book_id}")
def update_book(id: int, qwestion: LevelSchema, db: Session = Depends(get_db)):
    up_qwestion = db.query(Level).filter(Level.id == id).first()
    if not up_qwestion:
        raise HTTPException(status_code=404, detail="Qwestion not found")
    up_qwestion.section_name = qwestion.section_name
    up_qwestion.question = qwestion.question
    up_qwestion.answer = qwestion.answer
    db.commit()
    return {"message": "Qwestion updated"}


@router_level_test.delete("/delete-qwestion/{qwestion_id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    del_qwestion = db.query(Level).filter(Level.id == id).first()
    if not del_qwestion:
        raise HTTPException(status_code=404, detail="Qwestion not found")
    db.delete(del_qwestion)
    db.commit()
    return {"message": "Qwestion deleted"}
