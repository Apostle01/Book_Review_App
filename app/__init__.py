from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your_secret_key")

    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri or "postgresql://postgres:Admin@localhost/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes import app_bp
    app.register_blueprint(app_bp)

    return app


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import Config
# # import os

# # if os.path.exists("env.py"):
# #     import env

# db = SQLAlchemy()

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(app.config.Config)

#     # Initialize the database
#     db.init_app(app)

#     # with app.app_context():
#     #     db.create_all()

#     # Register Blueprints here if you have any
#     from .routes import main
#     app.register_blueprint(main)

#     return app


# # app/__init__.py
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# # from flask_login import LoginManager

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('app.config.Config')

#     db.init_app(app)
#     migrate.init_app(app, db)

#     with app.app_context():
#         from . import routes
#         db.create_all()

#     return app
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager

# db = SQLAlchemy()
# migrate = Migrate()
# login = LoginManager()

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech/alive_tank_path_776536'
#     app.config['SECRET_KEY'] = 'f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60'

#     db.init_app(app)
#     migrate.init_app(app, db)
#     login.init_app(app)

#     from app import routes, models
#     app.register_blueprint(routes.bp)

#     return app