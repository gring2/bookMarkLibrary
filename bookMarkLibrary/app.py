import os
from flask import Flask, render_template, send_from_directory
from flask_security import Security, SQLAlchemyUserDatastore
from bookMarkLibrary.models import User
from bookMarkLibrary.send_storage_file import SendStorageFileHandler
from flask_wtf.csrf import CSRFProtect
from bookMarkLibrary.database import init_db, db, set_db_config
from bookMarkLibrary.const import register_const

send_storage_handler = SendStorageFileHandler()
csrf = CSRFProtect()
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app: Flask = Flask(__name__, instance_relative_config=True)
user_datastore = SQLAlchemyUserDatastore(db, User, None)


def create_app(test_config=None):
    # create and configure the app
    csrf.init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        STORAGE_PATH=app.root_path + '/storage',
        SECURITY_REGISTERABLE=True,
        SECURITY_SEND_REGISTER_EMAIL= False
    )
    # flask-security configuration mapping
    app.config.from_mapping(
        SECURITY_REGISTERABLE=True,
        SECURITY_SEND_REGISTER_EMAIL=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        set_db_config(app)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    init_db(app)

    try:
        graceful_create_dir(app.instance_path)
        graceful_create_dir(app.config['STORAGE_PATH'])
    except OSError:
        pass

    @app.before_request
    def register_g_value():
        register_const()

    @app.route('/')
    def home():
        return render_template('index.html')

    import library
    app.register_blueprint(library.bp)

    def send_storage_file(filename):
        cache_timeout = send_storage_handler.get_send_file_max_age(filename)
        return send_from_directory(app.config['STORAGE_PATH'], filename,
                                   cache_timeout=cache_timeout)

    app.add_url_rule('/storage/<path:filename>', endpoint='storage',
                     view_func=send_storage_file)
    # Setup Flask-Security
    security = Security(app, user_datastore)


    return app


def graceful_create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)



