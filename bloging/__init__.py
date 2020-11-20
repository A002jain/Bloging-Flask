import os
from flask import Flask , url_for ,g
from . import db, auth, blog
def create_app(test_config = None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY= 'dev',DATABASE=os.path.join(app.instance_path,'blogdb.sqlite'))
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

    @app.route('/getappData')
    def getappData():
        for i in g:
            print(i)           
        return str(g.get("user")[0])

    #init db with the flask app
    db.init_app(app)

    # register auth blueprint
    app.register_blueprint(auth.bp)

    #register blog blueprint
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


    return app



# if everthing is correct still facing noApp error 
# then issue is arising because __init__.py is not recognised as init file so not
# recognising bloging as a package