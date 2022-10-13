from flask import Flask, render_template, flash, redirect
from config import Config
from forms import LoginForm
from flask_bootstrap import Bootstrap

application = Flask(__name__)
app = application
Bootstrap(app)
app.config.from_object(Config)
@app.route('/')
def home():
	return 'Hi'
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'Login requested for user {form.username.data}.')
		return redirect('/appwelcome')
	return render_template('login.html', title='Login', form=form)
@app.route('/appwelcome')
def app_welcome():
	return "You have logged in successfully!"
