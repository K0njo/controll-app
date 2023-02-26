from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from src.database_connection import get_db
from src.models.user import schemas
from src.models.user.models import User
from src.models.user.schemas import UserCreate
from src.auth.manager import (get_password_hash, authenticate_user, create_access_token,
                              get_current_token, invalid_tokens)

router = APIRouter(
    tags=["authentication", ]
)


@router.post("/register/", response_model=schemas.UserDisplay)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Register a new user.

    This endpoint creates a new user account in the database.

    Parameters:
    - **payload**: request body containing user data.
    - **db**: database connection object.

    Returns:
    - **200 OK**: Returns JSON response containing the newly registered user's data.
    - **400 Bad Request**: If the username or email is already registered.
    """
    db_user = db.query(User).filter(User.username == payload.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    db_user = db.query(User).filter(User.email == payload.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user_dict = payload.dict()
    user_dict["hash_password"] = get_password_hash(payload.password.get_secret_value())
    del user_dict["password"]
    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token/")
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
        Obtain an access token for an authenticated user.

        This endpoint authenticates a user based on their username and password, and issues
        an access token that can be used to access protected resources.

        Parameters:
        - **form_data**: form data containing the user's username and password.
        - **db**: database connection object.

        Returns:
        - **200 OK**: Returns a JSON response containing the access token and token type.
        - **401 Unauthorized**: If the username or password is invalid.
        """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token_expires_delta = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, user.role, expires_delta=token_expires_delta)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout/")
def logout_access_token(token: str = Depends(get_current_token)):
    """
        Log out a user by invalidating their access token.

        This endpoint invalidates the access token of a logged-in user, effectively logging
        them out of the system.

        Parameters:
        - **token**: access token for the user.

        Returns:
        - **200 OK**: Returns a JSON response indicating that the user has been successfully logged out.
        """
    invalid_tokens.add(token)
    return {"detail": "Successfully logged out"}
