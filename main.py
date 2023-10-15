from datetime import datetime

import pytz
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from Database.request_models import UserRequest
from config import Config
from db import get_db, get_user, create_user
from utils import create_access_token, create_refresh_token, verify_password

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    response = {
        "detail": "Некорректный формат email"
    }
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Перепроверьте подключение к сети"}
    )


@app.post('/register')
async def register(data: UserRequest, db: Session = Depends(get_db)):
    if data.invitation_code == Config.INVITATION_CODE:
        try:
            user = get_user(data.login, db)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Перепроверьте подключение к данным")
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким логином уже существует!"
            )
        try:
            return create_user(data, db)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Перепроверьте подключение к данным")
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неправильный пригласительный код"
        )


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(form_data.username, db)
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
    current_time_utc = datetime.now()
    time_difference = current_time_utc - user.date_registration
    if time_difference.days > 270:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )
    create_access_token(user.login)
    create_refresh_token(user.login)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "http://diacompanion.ru/download"}
    )


@app.post('/download')
@app.get('/download')
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/ping")
async def ping():
    return {"pong"}

# schedule.every().days(30).do(generate_random_string(100))
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
