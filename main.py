from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from flask import jsonify, render_template, Flask, request, flash
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import Session
from starlette import status
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.templating import Jinja2Templates

from Database.request_models import UserRequest
from config import Config
from db import get_db, get_user, create_user
from forms import LoginForm
from utils import create_access_token, create_refresh_token, verify_password

app = FastAPI()
flask_app = Flask(__name__)
flask_app.secret_key = 'f3cfe9ed8fae309f02079dbf'
bootstrap = Bootstrap(flask_app)

app.mount("/register", WSGIMiddleware(flask_app))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    response = {
        "detail": "Некорректный формат email"
    }
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response)


@app.exception_handler(Exception)
async def exception_handler(request_exception: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Перепроверьте подключение к сети"}
    )


def register(data: UserRequest):
    if data.code == Config.INVITATION_CODE:
        user = get_user(data.login)
        if user is not None:
            flash("Пользователь с таким логином уже существует!")
        return create_user(data)
    else:
        flash("Неправильный пригласительный код")


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


@flask_app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserRequest(
            login=form.username.data,
            password=form.password.data,
            code=form.invitation_code.data
        )
        return register(user)
    return render_template('authorization.html', form=form)

# @flask_app.route('/register')
# def register(login, password):
#     user = User.query.filter_by(login=login).first()
#     if user is None and login is not None:
#         user = User(login=login, password=password, date_registration=datetime.utcnow())
#         db.session.add(user)
#         db.session.commit()
#         flash("Успех!")
#         status_code = 200
#         response = jsonify({"status_code": status_code})
#         response.status_code = status_code
#         return response
#     else:
#         flash("Пользователь с таким логином уже существует")
#         status_code = 404
#         response = jsonify({"status_code": status_code})
#         response.status_code = status_code
#         return response


@app.get("/ping")
async def ping():
    return {"pong"}

# schedule.every().days(30).do(generate_random_string(100))
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
