from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Class containing wtforms objects for forms"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    photo = SelectField('Photo', choices=[('1', 'Monke'), ('2', 'Ber'), ('3', 'Cat'), ('4', 'Fox')])
    submitNickname = SubmitField('Save changes')
    submitPhoto = SubmitField('Save changes')

class UserForm(FlaskForm):
    accountID = StringField('Account ID', validators=[DataRequired()])
    dateOfBirth = StringField('Date of Birth', validators=[DataRequired()])
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    username = StringField('Account username', validators=[DataRequired()])
    password = StringField('Account password', validators=[DataRequired()])
    submit1 = SubmitField('Log In')

