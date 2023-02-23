# from datetime import timedelta
#
# from fastapi import Depends, APIRouter
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from starlette import status
#
# from src.database_connection import get_db
# from src.auth.authentication import get_password_hash, authenticate_user, create_access_token, get_token_exception
# import src.models.user.user_model as model
# from src.models.user.user_schema import UserSchema
#
# router_auth = APIRouter(
#     prefix='/user',
#     tags=['user']
# )
#
#
# @router_auth.post("/create/user")
# async def create_user(create_user: UserSchema, db: Session = Depends(get_db)):
#     print(f'CreateUser : %s' % create_user)
#
#     create_user_model = model.User()
#
#     create_user_model.username = create_user.username
#     create_user_model.email = create_user.email
#     create_user_model.first_name = create_user.first_name
#     create_user_model.last_name = create_user.last_name
#
#     hash = get_password_hash(create_user.password)
#     print('\n\n hash: %s' % hash)
#
#     create_user_model.hash_password = hash
#     create_user_model.is_active = True
#
#     print(f'\n\nCreateUser MODEL AFTER: %s' % create_user_model)
#
#     db.add(create_user_model)
#     db.commit()
#
#
# @router_auth.post("/token")
# async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
#                              db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         return get_token_exception(), status.HTTP_401_UNAUTHORIZED
#
#     token_expires_delta = timedelta(minutes=20)
#     token = create_access_token(user.username, user.id, expires_delta=token_expires_delta)
#
#     return {"access_token": token, "token_type": "bearer"}
