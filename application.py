from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from questionForm import answerForm

application = Flask(__name__)
app = application
Bootstrap(app)
app.config.from_pyfile("config.py")

@app.route('/')
def home():
	return 'Hi there'

@app.route('/game', methods=['GET', 'POST'])
def game():
	answerform = answerForm()
	if answerform.validate_on_submit():
		if answerform.answer.data==answerform.answers:
			flash("Correct!")
		
	return render_template('game.html', title='Game', form=answerform)