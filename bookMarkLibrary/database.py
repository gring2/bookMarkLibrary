import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:////' + os.path.join(app.instance_path, 'bookmark.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SECURITY_PASSWORD_SALT'] = 'salty'

    db.init_app(app)
    Migrate(app, db)

