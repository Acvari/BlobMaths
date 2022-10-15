from flask import Flask, render_template, flash, redirect
from config import Config
from forms import LoginForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user
from user_placeholder import User
application = Flask(__name__)
app = application
login = LoginManager(app)
Bootstrap(app)
login.init_app(app)
app.config.from_object(Config)
user = User()

@login.user_loader
def load_user(id):
	return user

@app.route('/')
def home():
	return 'Hi'
@app.route('/login', methods=['GET', 'POST'])
def login():
	print(current_user)
	if current_user.is_authenticated:
		return redirect('/appwelcome')
	form = LoginForm()
	if form.validate_on_submit():
		if (form.username.data != 'Batting Chestum') and (form.password.data != 'bigload420'):
			flash(f'Incorrect login requested for user {form.username.data}.')
			return redirect('/login')
		login_user(user)
		return redirect('/appwelcome')
	return render_template('login.html', title='Login', form=form)
@app.route('/appwelcome')
def app_welcome():
	return "You have logged in successfully!"
