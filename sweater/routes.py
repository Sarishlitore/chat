from datetime import datetime

from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from sweater import app, db
from sweater.models import User, Message, Chat, UserChatRelation


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        user_login = request.form['login']
        user = User(first_name=first_name, last_name=last_name, login=user_login)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except SQLAlchemyError as error:
            return error
    else:
        return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_login = request.form['login']
        user = User.query.filter_by(login=user_login).first()
        if user is not None:
            return redirect(url_for('user_info', user_id=user.id))
        else:
            return "Неправильный логин"
    else:
        return render_template('login.html')


@app.route('/user/<int:user_id>')
def user_info(user_id):
    chats = db.session.query(UserChatRelation, Chat).join(Chat).filter(UserChatRelation.user_id == user_id).all()
    user = User.query.filter_by(id=user_id).first()
    return render_template('user.html', user=user, chats=chats)


@app.route('/user/<int:user_id>/new_chat', methods=['POST'])
def new_chat(user_id):
    chat_name = request.form['chatName']
    chat = Chat(name=chat_name)
    try:
        db.session.add(chat)
        db.session.commit()
    except SQLAlchemyError as error:
        return error
    user_chat_relation = UserChatRelation(user_id=user_id, chat_id=chat.id)
    try:
        db.session.add(user_chat_relation)
        db.session.commit()
    except SQLAlchemyError as error:
        return error
    return redirect(url_for('user_info', user_id=user_id))


@app.route('/user/<int:user_id>/<int:chat_id>')
def show_chat(user_id, chat_id):
    user = User.query.filter_by(id=user_id).first()
    chat = Chat.query.filter_by(id=chat_id).first()
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.date).all()
    return render_template('chat.html', user=user, chat=chat, messages=messages)


@app.route('/user/<int:user_id>/<int:chat_id>/messaging', methods=['POST'])
def messaging(user_id, chat_id):
    message_text = request.form['message_text']
    message = Message(author_id=user_id, chat_id=chat_id, text=message_text)

    try:
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('show_chat', user_id=user_id, chat_id=chat_id))
    except SQLAlchemyError as error:
        return error
