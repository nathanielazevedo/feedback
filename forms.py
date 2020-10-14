"""Forms for flask-feedback."""

from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional



class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(min=6, max=55)],
    )



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )



class FeedBackForm(FlaskForm):
    """Feedback form."""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
