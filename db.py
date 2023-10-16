from datetime import datetime

import pytz
from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from Database.models import User
from Database.request_models import UserRequest
from utils import get_hashed_password
from config import Config

SQLALCHEMY_DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


def get_user(login: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.login == login).first()


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
    return RedirectResponse("/download")
