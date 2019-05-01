import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(session_options={'autocommit': False})


def set_db_config(app):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
        **{
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', 'hoge'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('MYSQL_DATABASE', 'hoge'),
        })

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # SQLAlchemy


def init_db(app):
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SECURITY_PASSWORD_SALT'] = 'salty'

    db.init_app(app)
    Migrate(app, db)
