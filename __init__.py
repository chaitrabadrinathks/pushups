from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

## Function name should be create_app().. because when we export FLASK_APP env variable with project folder
## it looks for create_app to run inside init__.py
def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()  ## This object is used to hold the settings used for logging in. 
    login_manager.login_view = 'auth.login'    ####The name of the view to redirect to when the user needs to log in.
    login_manager.init_app(app) ## Configures an application

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))


    #### application to communicate with main.py when app runs. First time when app runs its calls init.py
    ####  So Registring blue print,, saying init ... 
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    ### We are making now auth.py to communicate with project.. So similar we are registreing here
    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User

    with app.app_context():
        db.create_all()

    return app

