from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SECRET_KEY'] = '8a5cbf0ba91803e047f5684c46ccf1f9a681b93f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

from sweater.UserLogin import UserLogin
from sweater.chatdb import ChatDB

db.create_all()
chatdb = ChatDB(db.session)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, chatdb)


from sweater import routes
