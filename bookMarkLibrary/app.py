import os
from flask import Flask, render_template, send_from_directory, g
from flask_security import Security, SQLAlchemyUserDatastore
from models import User
from bookMarkLibrary.send_storage_file import SendStorageFileHandler
from flask_wtf.csrf import CSRFProtect
from bookMarkLibrary.database import init_db, db, set_db_config
from bookMarkLibrary.const import register_const

send_storage_handler = SendStorageFileHandler()
csrf = CSRFProtect()
user_datastore = SQLAlchemyUserDatastore(db, User, None)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(test_config=None):
    # create and configure the app
    __setup_logging()
    # logging.basicConfig(filename=ROOT_DIR + '/../log/error.log')

    app = Flask(__name__, instance_relative_config=True)

    csrf.init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        STORAGE_PATH=app.root_path + '/storage',
        SECURITY_REGISTERABLE=True,
        SECURITY_SEND_REGISTER_EMAIL=False
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
        __graceful_create_dir(app.instance_path)
        __graceful_create_dir(app.config['STORAGE_PATH'])
    except OSError:
        pass

    @app.before_request
    def register_g_value():
        register_const()

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

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


#    @app.errorhandler(Exception):
    return app


def __setup_logging():
    import logging.config
    import yaml

    config = yaml.safe_load(open(ROOT_DIR + '/logging.conf'))

    def __set_root_path_to_filename(handlers):
        for k, handler in handlers.items():
            if 'filename' in handler:
                handler['filename'] = handler['filename'].replace('$ROOT_PATH', ROOT_DIR + '/..')
                handlers[k] = handler

    __set_root_path_to_filename(config['handlers'])

    logging.config.dictConfig(config)


def __graceful_create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
