from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

import src.models.user.crud as crud
import src.models.user.schemas as schemas
from src.database_connection import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{user_id}/", response_model=schemas.UserDisplay)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


@router.get("/name/{user_name}/", response_model=schemas.UserDisplay)
def get_user_by_name(user_name: str, db: Session = Depends(get_db)):
    return crud.get_user_by_name(db, user_name)


@router.get("/email/{user_email}/", response_model=schemas.UserDisplay)
def get_user_by_email(user_email: EmailStr, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db, user_email)


@router.get("/all/", response_model=list[schemas.UserDisplay])
def get_users(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, page, page_size)


@router.post("/new/", response_model=schemas.UserDisplay)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user_data)


@router.patch("/{user_id}/", response_model=schemas.UserDisplay)
def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, user_data)


@router.delete("/{user_id}/", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


@router.put("/{user_id}/block/", response_model=dict)
def block_user(user_id: int, db: Session = Depends(get_db)):
    return crud.block_user(db, user_id)


@router.put("/{user_id}/unblock/", response_model=dict)
def unblock_user(user_id: int, db: Session = Depends(get_db)):
    return crud.unblock_user(db, user_id)


@router.put("/{user_id}/activate/", response_model=dict)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    return crud.activate_user(db, user_id)


@router.put("/{user_id}/deactivate/", response_model=dict)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    return crud.deactivate_user(db, user_id)


@router.put("/{user_id}/role/", response_model=dict)
def update_role(user_id: int, role: schemas.Role, db: Session = Depends(get_db)):
    return crud.update_role(db, user_id, role)
