# from datetime import datetime, timedelta
# from typing import Optional
#
# from fastapi import HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from starlette import status
#
# from src.models.user.user_model import User
# from passlib.context import CryptContext
#
# bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# SECRET_KEY = ']%>w3KcCL=oNgkyduW^8Q35*^TrPT*W!3K}'
# ALGORITHM = 'HS256'
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         id: int = payload.get("id")
#         if username is None or id is None:
#             raise get_user_exeption()
#
#         return {"username": username, "id": id}
#     except JWTError:
#         raise get_user_exeption()
#
#
# def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
#     to_encode = {"sub": username, "id": user_id}
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#
# def authenticate_user(username: str, password: int, db):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return False
#     if not verify_password(password, user.hash_password):
#         return False
#     return user
#
#
# def verify_password(plain_password, hashed_password):
#     return bycrypt_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return bycrypt_context.hash(password)
#
#
# def get_user_exeption():
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     return credentials_exception
#
#
# def get_token_exception():
#     token_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     return token_exception
