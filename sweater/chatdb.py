from sqlalchemy.exc import SQLAlchemyError

from sweater.models import Users, Profiles, UserChatRelations, Chats, Messages


class ChatDB:
    def __init__(self, session):
        self.__session = session

    def add_user(self, name: str, email: str, hash_psw: str) -> bool:
        try:
            if Users.query.filter_by(email=email).first():
                print("Пользователь с таким email уже существует")
                return False
            user = Users(email=email, psw=hash_psw)
            self.__session.add(user)
            self.__session.flush()
            profile = Profiles(name=name, user_id=user.id)
            self.__session.add(profile)
            self.__session.commit()
        except SQLAlchemyError as err:
            print('Ошибка при добавление нового пользователя ' + str(err))
            return False
        return True

    @staticmethod
    def get_user(user_id: int):
        try:
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                print('Пользователь не найден')
                return False
            return user
        except SQLAlchemyError as err:
            print('Ошибка при получение данных из БД ' + str(err))
        return False

    @staticmethod
    def get_user_by_email(email):
        try:
            user = Users.query.filter_by(email=email).first()
            if not user:
                print('Пользователь не найден')
                return False
            return user
        except SQLAlchemyError as err:
            print('Ошибка при получение данных из БД ' + str(err))
        return False

    def get_chats(self, user_id):
        chats = self.__session.query(UserChatRelations, Chats).join(Chats). \
            filter(UserChatRelations.user_id == user_id).all()
        return chats

    def add_chat(self, name):
        try:
            chat = Chats(name=name)
            self.__session.add(chat)
            self.__session.commit()
        except SQLAlchemyError as err:
            print('Ошибка при добавление нового пользователя ' + str(err))
            return False
        return chat

    def add_user_to_chat(self, chat_id, user_id):
        try:
            user_chat_relation = UserChatRelations(user_id=user_id, chat_id=chat_id)
            self.__session.add(user_chat_relation)
            self.__session.commit()
        except SQLAlchemyError as err:
            print('Ошибка при добавление нового пользователя ' + str(err))
            return False
        return True

    @staticmethod
    def get_chat(chat_id):
        try:
            chat = Chats.query.filter_by(id=chat_id).first()
            if not chat:
                print('Чат не найден')
                return False
            return chat
        except SQLAlchemyError as err:
            print('Ошибка при получение данных из БД ' + str(err))
        return False

    @staticmethod
    def get_messages(chat_id):
        try:
            messages = Messages.query.filter_by(chat_id=chat_id).all()
            print(messages)
            if not messages:
                print('Чат не найден')
                return False
            return messages
        except SQLAlchemyError as err:
            print('Ошибка при получение данных из БД ' + str(err))
        return False

    def add_message(self, chat_id, author_id, text):
        try:
            message = Messages(chat_id=chat_id, author_id=author_id, text=text)
            self.__session.add(message)
            self.__session.commit()
        except SQLAlchemyError as err:
            print('Ошибка при добавление сообщения' + str(err))
            return False
        return message
