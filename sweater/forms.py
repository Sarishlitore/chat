from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField
from wtforms.validators import Email, DataRequired, Length, EqualTo, InputRequired
from wtforms.widgets import HiddenInput


class LoginForm(FlaskForm):
    email = EmailField('Email: ')
    psw = PasswordField('Пароль: ', validators=[InputRequired()])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField('Имя: ', validators=[InputRequired(message='Введите имя'),
                                            Length(min=1, max=64, message="Имя должно быть от 1 до 64 символов")])
    email = EmailField('Email: ')
    psw = PasswordField('Пароль: ', validators=[InputRequired(message='Введите пароль'),
                                                Length(min=4, max=20,
                                                       message="Пароль должен быть от 4 до 20 символов")])
    psw2 = PasswordField('Повтор пароля: ', validators=[InputRequired(message='Повторите пароль'),
                                                        EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Регистрация')


class ChatForm(FlaskForm):
    name = StringField('Название чата', validators=[InputRequired(message='Введите название чата')])
    submit = SubmitField('Создать')


class ChatUserForm(FlaskForm):
    chat_id = IntegerField(widget=HiddenInput())
    user_id = IntegerField(widget=HiddenInput())
    submit = SubmitField('Пригласить')


class MessageForm(FlaskForm):
    text = StringField('Сообщение')
    submit = SubmitField('Отправить')
