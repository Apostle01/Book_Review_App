from flask_sqlalchemy import SQLAlchemy
from . import db
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_link = db.Column(db.String(300))
    amazon_link = db.Column(db.String(300))
    comments = db.relationship('Comment', backref='book', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(60), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     author = db.Column(db.String(150), nullable=False)
#     details = db.Column(db.Text, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     image_link = db.Column(db.String(250))
#     amazon_link = db.Column(db.String(250))

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     book = db.relationship('Book', backref=db.backref('comments', lazy=True))


# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from datetime import datetime
# from app import db, login_manager

# db = SQLAlchemy()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class Users(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     books = db.relationship('Book', backref='owner', lazy=True)

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     author = db.Column(db.String(150), nullable=False)
#     details = db.Column(db.Text, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     image_link = db.Column(db.String(300), nullable=False)
#     amazon_link = db.Column(db.String(300), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     upvotes = db.Column(db.Integer, default=0)
#     book = db.relationship('Book', backref=db.backref('comments', lazy=True))

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     # Relationships and other fields

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     # Relationships and other fields
