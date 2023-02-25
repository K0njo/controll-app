from typing import Type, List
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy_pagination import paginate
from starlette import status

import src.models.user.models as models
import src.models.user.schemas as schemas


def get_user(db: Session, user_id: int) -> Type[models.User]:
    """
        Retrieve a single user by ID.

        Args:
            db (Session): The database session.
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user matching the specified ID.

        Raises:
            HTTPException: If no user is found with the specified ID.
       """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_user_by_name(db: Session, username: str) -> Type[models.User]:
    """
        Get a user from the database by username.

        Args:
            db (Session): The database session.
            username (str): The username of the user to get.

        Returns:
            User: The user with the specified username.

        Raises:
            HTTPException: If no user is found with the specified username.
        """
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_user_by_email(db: Session, email: EmailStr) -> Type[models.User]:
    """
        Get a user from the database by email.

        Args:
            db (Session): The database session.
            email (EmailStr): The email address of the user to get.

        Returns:
        User: The user with the specified email.

        Raises:
            HTTPException: If no user is found with the specified email.
        """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_users(db: Session, page: int = 1, page_size: int = 10) -> list[Type[models.User]]:
    """
    Get a list of users from the database, with optional pagination.

    Args:
        db (Session): The database session.
        page (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The maximum number of users to return per page. Defaults to 10.

    Returns:
        List[User]: A list of users.

    Raises:
        HTTPException: If there are no users in the database or if an error occurs while paginating.
    """
    print(page, page_size)
    query = db.query(models.User)
    print(query)
    try:
        users = paginate(query, page, page_size).items
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error while paginating users") from e

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No users found")
    print(users, type(users))
    return users


def delete_user(db: Session, user_id: int) -> dict:
    """
        Delete a user from the database.

        Args:
            db (Session): The database session.
            user_id (int): The ID of the user to delete.

        Returns:
            dict: A dictionary with the message indicating the success of the operation.

        Raises:
            HTTPException: If the user is not found in the database.
        """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User successfully deleted"}


def block_user(db: Session, user_id: int) -> dict:
    """
        Block a user with the provided user_id in the database.

        Parameters:
            db (Session): The SQLAlchemy database session.
            user_id (int): The ID of the user to block.

        Returns:
            dict: A dictionary with a success message.

        Raises:
            HTTPException: If the user is not found or if the user is already blocked.
        """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_blocked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already blocked")
    user.is_blocked = True
    db.commit()
    db.refresh(user)
    return {"message": "User blocked successfully"}


def unblock_user(db: Session, user_id: int) -> dict:
    """
        Unblock a user with the provided user_id in the database.

        Parameters:
            db (Session): The SQLAlchemy database session.
            user_id (int): The ID of the user to unblock.

        Returns:
            dict: A dictionary with a success message.

        Raises:
            HTTPException: If the user is not found or if the user is not blocked.
        """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_blocked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not blocked")
    user.is_blocked = False
    db.commit()
    return {"detail": "User has been unblocked."}


def activate_user(db: Session, user_id: int) -> dict:
    """
        Activates the user with the provided user_id in the database.

        Parameters:
            db (Session): The SQLAlchemy database session.
            user_id (int): The ID of the user to activate.

        Returns:
            dict: A dictionary with a success message.

        Raises:
            HTTPException: If the user is not found or if the user is already active.
        """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already activated")
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User activated successfully"}


def deactivate_user(db: Session, user_id: int) -> dict:
    """
        Deactivate the user with the provided user_id in the database.

        Parameters:
            db (Session): The SQLAlchemy database session.
            user_id (int): The ID of the user to deactivate.

        Returns:
            dict: A dictionary with a success message.

        Raises:
            HTTPException: If the user is not found or if the user is already inactive.
        """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already inactive")
    else:
        user.is_active = False
        db.commit()
        db.refresh(user)
        return {"message": "User deactivated successfully"}


def update_role(db: Session, user_id: int, role: schemas.Role) -> dict:
    """
    Update a user's role in the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        role (Role): The new role for the user.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the user is not found in the database.

    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    setattr(user, "role", role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Role updated successfully"}


