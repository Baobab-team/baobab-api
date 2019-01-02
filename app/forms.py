
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from app.models.users import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()],
                        render_kw={"class": "input is-large", "type": "email", "placeholder": "Your Email"}
                        )
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={"class": "input is-large", "type": "password", "placeholder": "Your Password"}
                             )

    remember = BooleanField( "Remember me")


class BusinessFormAdd(FlaskForm):
    email = StringField('email', validators=[DataRequired()],
                        render_kw={"class": "input is-large", "type": "email", "placeholder": "Your Email"}
                        )
    name = StringField('name', validators=[DataRequired()],
                        render_kw={"class": "input is-large", "type": "email", "placeholder": "Business name"}
                        )
