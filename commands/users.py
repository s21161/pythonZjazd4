from users import users_service
from database import database
from main import db_path
from datetime import datetime, timedelta
from exceptions import RegisterExceptions, LoginExceptions
import jwt


def register_command(login, password):
    if not validate(login, password):
        raise RegisterExceptions("wrong login or password")
    db = database.get_database(db_path).cursor()
    if users_service.has_user(db, login):
        raise RegisterExceptions("user exist")
    users_service.create_user(db, login, password)


def login_command(login, password):
    if not validate(login, password):
        raise LoginExceptions("wrong_data")
    db = database.get_database(db_path).cursor()
    user = users_service.login(db, login, password)
    if user is None:
        raise LoginExceptions("wrong_login")
    else:
        return user


def validate(login, password):
    if login is None or password is None:
        return False
    if not users_service.validate_login(login):
        return False
    if not users_service.validate_password(password):
        return False
    return True


jwt_secret = "asdadaaeaounaobapsdzczknoaebfapqzmcalq2mnsd"


def token_authorization(login, password, user_id, exp_time=15):
    load_data = {
        "login": login,
        "password": password,
        "exp": datetime.utcnow() + timedelta(minutes=exp_time),
        "sub": user_id
    }
    return jwt.encode(payload=load_data, key=jwt_secret)


def token_decoder(tokens):
    try:
        return jwt.decode(tokens, key=jwt_secret, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        return False
    except jwt.exceptions.ExpiredSignatureError:
        return False
