from datetime import datetime

from sweater import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    psw = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f'<User {self.id}>'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Profile {self.id}>'


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('Users', backref='messages', uselist=False)

    def __repr__(self):
        return f'<Message {self.id}>'


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Chats {self.id}>'


class UserChatRelations(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), primary_key=True)

    def __repr__(self):
        return f'<UserCharRelation {self.user_id, self.chat_id}>'
