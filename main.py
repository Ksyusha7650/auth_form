from datetime import datetime

import pytz
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from db import get_db
from api.models import UserRequest
from Database.models import User
from utils import get_hashed_password, create_access_token, create_refresh_token, verify_password

app = FastAPI()


@app.post("/")
def create_user(details: UserRequest, db: Session = Depends(get_db)):
    current_time_utc = datetime.now(pytz.utc)
    time_utc3 = current_time_utc.astimezone(pytz.timezone('Europe/Moscow'))
    to_create = User(
        login=details.login,
        password=get_hashed_password(details.password),
        date_registration=time_utc3
    )
    db.add(to_create)
    db.commit()
    return {
        "success": True,
        "created_id": to_create.id
    }


@app.get("/")
def get_by_login(login: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.login == login).first()


@app.post('/register', summary="Create new user")
async def register(data: UserRequest, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = get_by_login(data.login, db)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    return create_user(data, db)


@app.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_by_login(form_data.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильный логин или пароль"
        )
    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильный логин или пароль"
        )

    return {
        "access_token": create_access_token(user.login),
        "refresh_token": create_refresh_token(user.login),
    }
