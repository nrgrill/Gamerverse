from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from gamerverse.config import Config
from flask_mail import Mail
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['MAIL_SERVER'] = 'stmp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'thegamerversehelp@gmail.com'
    app.config['MAIL_PASSWORD'] = 'makeuc2023' 
    mail = Mail(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from gamerverse.users.routes import users
    from gamerverse.posts.routes import posts
    from gamerverse.main.routes import main
    from gamerverse.models import User
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    with app.app_context():
        db.create_all()
    usernames = ['Nathan Grilliot', 'Alex Bell', 'RyanC', 'Clara Gehm']
    emails = ['nrgrill2003@gmail.com', 'bellalexj11@gmail.com', 'rcoor6337@gmail.com', 'cjgehm@gmail.com']
    images = ['default.jpg', 'default.jpg', 'default.jpg', 'default.jpg']
    passwords = ['$2b$12$8r4DcnkA0jAM/aHJ4Hfr4.UkMbgCP5T7FBbsBQ3OrU2rbn5VjzppW', '$2b$12$XMSIVnQXxTAU2ffTqpKdxuJYSQQ9dSYmNZncDUmZGevwG3z8tWoDS', '$2b$12$Ww.19oSjvFByMi.jVtwWNO45yqI5JkmWIfWsiByV/TmWxa0sTyqyK', '$2b$12$8vBHAPNYYMNCn9ssit/yAOKc99PePAQm1p2vdxboQrToyCVPzc0ZK']
    

    return app

