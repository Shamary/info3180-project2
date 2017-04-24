from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    fname=StringField('First Name',validators=[InputRequired]);
    lname=StringField('last Name',validators=[InputRequired]);
    age=IntegerField('age',validators=[InputRequired])
    gender=SelectField('gender',choices=['M','F','Other'])
    username = StringField('email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    ispassword = PasswordField('Confirm Password', validators=[InputRequired()])