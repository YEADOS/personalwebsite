import os
from flask import Flask 

def create_app():
    # instance_relative_config=True is used to have the configuration files outside the main application directory. This is important for things like the database and secret keys that should not be in main directory
    app = Flask(__name__, instance_relative_config=True)


    # config app using dictionary (key, value pairs)
    app.config.from_mapping(
        # SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'website.sqlite')
    )

    # config app from external python file. better 
    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    return app

