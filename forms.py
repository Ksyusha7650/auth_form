from flask_wtf import FlaskForm
from wtforms import PasswordField, validators, EmailField


class LoginForm(FlaskForm):
    username = EmailField('Логин',
                          [validators.DataRequired("Необходимо заполнить это поле"), validators.Email()])
    password = PasswordField('Пароль',
                             [validators.DataRequired("Необходимо заполнить это поле"), validators.Length(min=5, max=15,
                                                                                                          message="Пароль должен быть от 5 до 15 символов")])
    invitation_code = PasswordField('Пригласительный код',
                                    [validators.DataRequired("Необходимо заполнить это поле")])
