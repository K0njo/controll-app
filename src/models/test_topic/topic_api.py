import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from src.auth.authentication_api import get_db
from src.models.test_topic.topic_model import Topic
from src.models.test_topic import topic_model as model
from src.models.test_topic.topic_schema import TopicSchema

router_topic = APIRouter(prefix="/topic_test")


@router_topic.get("/topics/{topic_id}")
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()

    answers = list(topic.answer.values())
    random.shuffle(answers)

    response = {"question": topic.question, "answer": answers}

    return response


@router_topic.post("/new-topic/")
def new_topic(new_topic: TopicSchema, db: Session = Depends(get_db)):

    create_topic_model = model.Topic()

    create_topic_model.question = new_topic.question
    create_topic_model.answer = new_topic.answer

    try:
        db.add(create_topic_model)
        db.commit()
    except IntegrityError:
        raise HTTPException (status_code=400,detail='Topic already exists')

    return 'Topic has been created'


@router_topic.put("/topic-update/{topic_id}")
def update_topic(id: int, topic: TopicSchema, db: Session = Depends(get_db)):
    update_topic = db.query(Topic).filter(Topic.id == id).first()

    if not update_topic:
        raise HTTPException (status_code= 404, detail="Topic doesn't exist")

    update_topic.question = topic.question
    update_topic.answer = topic.answer

    db.commit()

    return "Topic has been updated"

@router_topic.delete("/topic-delete/{topic_id}")
def delete_topic(id: int, db: Session = Depends(get_db)):
        topic = db.query(Topic).filter(Topic.id == id).first()

        if not topic:
            raise HTTPException (status_code=404, detail="Topic doesn't exist")

        db.delete(topic)
        db.commit()

        return 'Topic has been deleted'