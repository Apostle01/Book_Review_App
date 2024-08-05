from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
# from app.models import Users

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    details = TextAreaField('Details', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image_link = StringField('Image Link')
    submit = SubmitField('Add Book')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Comment')


# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, BooleanField
# from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
# # from app.models import Users

# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')

# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')

#     def validate_username(self, username):
#         from app.models import Users  # Import here to avoid circular dependency
#         user = Users.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is taken. Please choose a different one.')

# class BookForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     author = StringField('Author', validators=[DataRequired()])
#     details = TextAreaField('Details', validators=[DataRequired()])
#     price = FloatField('Price', validators=[DataRequired()])
#     image_link = StringField('Image Link')
#     submit = SubmitField('Add Book')

# class CommentForm(FlaskForm):
#     content = TextAreaField('Content', validators=[DataRequired()])
#     submit = SubmitField('Add Comment')

# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, 
# FloatField, URLField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
# from app.models import User

# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')

#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is taken. Please choose a different one.')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one.')

# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')

# class UpdateAccountForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Update')

#     def validate_username(self, username):
#         if username.data != current_user.username:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError('That username is taken. Please choose a different one.')

#     def validate_email(self, email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError('That email is taken. Please choose a different one.')
