from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from sweater import app, chatdb, UserLogin
from sweater.forms import LoginForm, RegistrationForm, ChatForm, ChatUserForm, MessageForm
from sweater.models import Chats


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        hash_psw = generate_password_hash(form.psw.data)
        if chatdb.add_user(name=form.name.data, email=form.email.data, hash_psw=hash_psw):
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('index'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    return render_template('registration.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = chatdb.get_user_by_email(form.email.data)
        if user and check_password_hash(user.psw, form.psw.data):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('profile'))
    return render_template('login.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/chats', methods=['POST', 'GET'])
@login_required
def chats():
    chat_new_user = ChatUserForm()
    new_chat_form = ChatForm()
    if new_chat_form.validate_on_submit():
        chat = chatdb.add_chat(new_chat_form.name.data)
        chatdb.add_user_to_chat(chat_id=chat.id, user_id=current_user.get_id())
    if chat_new_user.validate_on_submit():
        chatdb.add_user_to_chat(chat_id=chat_new_user.chat_id.data, user_id=chat_new_user.user_id.data)
    return render_template('chats.html', cht_usr_form=chat_new_user, cht_form=new_chat_form,
                           chats=chatdb.get_chats(current_user.get_id()))


@app.route('/chats/<int:chat_id>', methods=['POST', 'GET'])
@login_required
def show_chat(chat_id):
    chat = chatdb.get_chat(chat_id)
    messages = chatdb.get_messages(chat_id)
    message_form = MessageForm()
    if message_form.validate_on_submit():
        message = chatdb.add_message(chat_id=chat.id, author_id=current_user.get_id(), text=message_form.text.data)
    return render_template('chat.html', message_form=message_form, chat=chat, messages=messages)

    #
    # @app.route('/new_chat', methods=['POST', 'GET'])
    # @login_required
    # def new_chat():
    #     form = ChatForm()
    #     if form.validate_on_submit():
    #         chat = chatdb.add_chat(form.name.data)
    #         chatdb.add_user_to_chat(chat_id=chat.id, user_id=current_user.get_id())
    #     return render_template('user.html', form=form, chats=chatdb.get_chats(current_user.get_id()))

    # @app.route('/user/<int:user_id>/<int:chat_id>')
    # def show_chat(user_id, chat_id):
    #     user = Users.query.filter_by(id=user_id).first()
    #     chat = Chats.query.filter_by(id=chat_id).first()
    #     messages = Messages.query.filter_by(chat_id=chat_id).order_by(Messages.date).all()
    #     return render_template('chats.html', user=user, chat=chat, messages=messages)
    #
    #
    # @app.route('/user/<int:user_id>/<int:chat_id>/messaging', methods=['POST'])
    # def messaging(user_id, chat_id):
    #     message_text = request.form['message_text']
    #     message = Messages(author_id=user_id, chat_id=chat_id, text=message_text)
    #
    #     try:
    #         db.session.add(message)
    #         db.session.commit()
    #         return redirect(url_for('show_chat', user_id=user_id, chat_id=chat_id))
    #     except SQLAlchemyError as error:
    #         return error
    #
    #
    # @app.route('/user/<int:user_id>/chat/<int:chat_id>/add_user', methods=['POST'])
    # def add_user_to_chat(user_id, chat_id):
    #     new_user_id = request.form['new_user']
    #     user_chat_relation = UserChatRelations(user_id=new_user_id, chat_id=chat_id)
    #     try:
    #         db.session.add(user_chat_relation)
    #         db.session.commit()
    #     except SQLAlchemyError as error:
    #         return error
    #     return redirect(url_for('show_chat', user_id=user_id, chat_id=chat_id))

#
# <form method="post" class="container">
#                     {{ cht_usr_form.hidden_tag() }}
#                     {{ cht_usr_form.chat_id(value=chat[1].id) }}
#                     {{ cht_usr_form.user_id(value=current_user.get_id()) }}
#                     {{ cht_usr_form.submit() }}
#                 </form>
