from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from src.database_connection import get_db
from src.models.books.book_model import Book
from src.models.books.book_schema import CreateBook

router_book = APIRouter(prefix="/book")


@router_book.get("/found-book/")
def get_book(book_name: str, db: Session = Depends(get_db)):
    book_name = db.query(Book).filter(Book.book_name == book_name).first()
    if not book_name:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_name


@router_book.get("/all-book/")
def get_book(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    books = db.query(Book).offset(skip).limit(page_size).all()
    return {"books": books}


@router_book.get("/{book_id}/download-book")
def download_book(book_id: int, db: Session = Depends(get_db)):
    file_book = db.query(Book).filter(Book.id == book_id).first()
    if not file_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return FileResponse(path=file_book.linker, filename=file_book.book_name, media_type='application/msword')


@router_book.post("/add-book/")
def post_book(book_add: CreateBook, db: Session = Depends(get_db)):
    new_book = Book(book_name=book_add.book_name,
                    author=book_add.author,
                    release_year=book_add.release_year,
                    book_description=book_add.book_description,
                    linker=book_add.linker)

    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Book already exists")

    return {"message": "Created"}


@router_book.put("/update-book/{book_id}")
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


@router_book.delete("/delete-book/{book_id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}
