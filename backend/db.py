from dotenv import load_dotenv
from functools import wraps
from sqlalchemy import *
from sqlalchemy.orm import *
from os import getenv

load_dotenv()
engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(
    getenv('MYSQL_DB_USER'),
    getenv('MYSQL_DB_PASS'),
    getenv('MYSQL_DB_HOST'),
    getenv('MYSQL_DB_NAME')
))
session_factory = sessionmaker(bind=engine)

def needs_db(var_name):
    def _db_deco(func):
        @wraps(func)
        def __db_deco(*args, **kwargs):
            scoped_sess = scoped_session(session_factory)
            kwargs[var_name] = scoped_sess()
            print(kwargs)
            result = func(*args, **kwargs)
            scoped_sess.commit()
            scoped_sess.remove()
            return result
        return __db_deco
    return _db_deco
