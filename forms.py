from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
