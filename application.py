from flask import Flask, render_template, flash, redirect
from secret import Config
from forms import LoginForm
from forms import ProfileForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user
from user_placeholder import User
from questionForm import answerForm

# initialise application
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
	return redirect('/login')


@app.route('/game', methods=['GET', 'POST'])
def game():
	print(current_user.nickname)
	answerform = answerForm()
	flash(f"Hello " + user.nickname)
	if answerform.validate_on_submit():
		if answerform.answer.data == answerform.answers:
			flash("Correct!")
		else:
			flash("Not Quite!")

	return render_template('game.html', title='Game', form=answerform)


@app.route('/login', methods=['GET', 'POST'])
def login():
	print(current_user)
	if current_user.is_authenticated:
		return redirect('/game')
	form = LoginForm()
	if form.validate_on_submit():
		if (form.username.data != 'a') and (form.password.data != 'a'):
			flash(f'Incorrect login requested for user {form.username.data}.')
			return redirect('/login')
		login_user(user)
		return redirect('/moduleSelection')
	return render_template('login.html', title='Login', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
	print(user.nickname)
	print(user.photo)
	form = ProfileForm()
	if form.validate_on_submit():
		user.nickname = form.nickname.data
		user.photo = form.photo.data
		if form.nickname.data == '':
			flash('Please choose a nickname!')
			return redirect('/profile')
		else:
			return redirect('/game')
	return render_template('profile.html', title='Profile', form=form)


@app.route('/moduleSelection', methods=['GET', 'POST'])
def module_selection():
	return render_template('moduleSelection.html', title='Module Selection')


if __name__ == "__main__":
	app.run()
