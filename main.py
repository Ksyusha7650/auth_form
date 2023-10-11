from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db import get_db, get_user, create_user
from Database.request_models import UserRequest
from Database.models import User
from deps import get_current_user
from utils import get_hashed_password, create_access_token, create_refresh_token, verify_password

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post('/register', summary="Create new user")
async def register(data: UserRequest, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = get_user(data.login, db)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )
    return create_user(data, db)


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
    create_access_token(user.login)
    create_refresh_token(user.login)
    return RedirectResponse("/download")


@app.get('/me', summary='Get details of currently logged in user')
async def get_me(user: User = Depends(get_current_user)):
    return user


@app.post('/download')
@app.get('/download')
async def index(request: Request):
    # return user
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="77.222.37.26")
