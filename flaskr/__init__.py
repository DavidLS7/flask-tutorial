import os

from flask import Flask

# this is a factory function, a design pattern for Flask apps
def create_app(test_config=None):
    # create and configure the app
    # this is the instantiated flask object
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/')
    def index():
        return 'Logged In'
    
    # Import and call this function from the factory. Place the new code at the end of the factory function before returning the app.
    def create_app():
        app = ...
    # My understanding is blueprints call the specific dependencies where they are required, for each controller and view
    from . import auth
    app.register_blueprint(auth.bp)

    from . import db
    db.init_app(app)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


    return app