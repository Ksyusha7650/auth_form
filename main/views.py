# from datetime import datetime
# from fastapi import templating
# from .forms import LoginForm
# from . import main
# from .. import db
# from ..models import User
#
#
# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = LoginForm()
#     check = False
#     if form.validate_on_submit():
#         if request.method == 'POST':
#             if request.form['submit_button'] == "enter":
#                 if login(form.username.data, form.password.data).status_code == 200:
#                     check = True
#             elif request.form['submit_button'] == "register":
#                 register(form.username.data, form.password.data)
#
#     if check:
#         status_code = 200
#         response = jsonify({"status_code": status_code})
#         response.status_code = status_code
#         return response
#     else:
#         return render_template('authorization.html', form=form)
#
#
# @main.route('/login/<login>=<password>')
# def login(login, password):
#     # login = request.args.get('login')
#     # password = request.args.get('password')
#     user = User.query.filter_by(login=login, password=password).first()
#     if user is None or login is None:
#         flash("Такого пользователя не существует или введен неправильный пароль")
#         status_code = 404
#         response = jsonify({"status_code": status_code})
#         response.status_code = status_code
#         return response
#     else:
#         status_code = 200
#         response = jsonify({"status_code": status_code})
#         response.status_code = status_code
#         return response
#
#
# @main.route('/register/<login>=<password>')
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
