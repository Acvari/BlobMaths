from flask import Flask, render_template
from flask_bootstrap import Bootstrap

application = Flask(__name__)
app = application
Bootstrap(app)

@app.route('/')
def home():
	return 'Hi there'

@app.route('/game')
def game():
	return render_template('base.html', title='Game')