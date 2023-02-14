from cffi import model
from fastapi import APIRouter, Depends, HTTPException
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from src.auth.authentication_api import get_db
from src.models.books.book_model import Book
from src.models.books.book_schema import CreateBook

router_book = APIRouter(prefix="/book")

@router_book.get("/found_book/")
def get_book(book_name: str, db: Session = Depends(get_db)):
    book_name = db.query(Book).filter(Book.book_name == book_name).first()
    if not book_name:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_name


@router_book.get("/all_book/")
def get_book(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"books": books}


@router_book.post("/add_book/")
def post_book(new_book: CreateBook, db: Session = Depends(get_db)):

    create_book_model = model.Book()

    create_book_model.book_name = new_book.book_name
    create_book_model.author = new_book.author
    create_book_model.release_year = new_book.release_year
    create_book_model.book_description = new_book.book_description
    create_book_model.linker = new_book.linker

    try:
        db.add(create_book_model)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Book already exists")

    return {"message": "Created"}



@router_book.put("/update_book/{book_id}")
def update_book(id: int, book: CreateBook, db: Session = Depends(get_db)):
    up_book = db.query(Book).filter(Book.id == id).first()
    if not up_book:
        raise HTTPException(status_code=404, detail="Book not found")
    up_book.book_name = book.book_name
    up_book.author = book.author
    up_book.release_year = book.release_year
    up_book.book_description = book.book_description
    up_book.linker = book.linker
    db.commit()
    return {"message": "Book updated"}


@router_book.delete("/delete_book/{book_id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}
