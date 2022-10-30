from awscli.errorhandler import ClientError
from awscli.paramfile import logger
from flask import Flask, render_template, flash, redirect, request, jsonify
from secret import Config
from forms import LoginForm
from forms import ProfileForm
from forms import UserForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user
from user_placeholder import User
from questionForm import answerForm
import boto3
from boto3.session import Session
import awscli
import json

# initialise application
# make static folder available on the root of the url '', get rid of the static/ part of static/new-admin.js
application = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
app = application
login = LoginManager(app)
Bootstrap(app)
login.init_app(app)
app.config.from_object(Config)
user = User()

# username: AKIAXOML5L575E3RVL3R
# password: qKa8Dzo6Mjee+vsejFMfi4+A3L3qa2CQB+a3Ggm0
dynamodb_session = Session(aws_access_key_id='AKIAXOML5L575E3RVL3R',
                           aws_secret_access_key='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',
                           region_name='eu-west-2')
database = dynamodb_session.resource("dynamodb", region_name="eu-west-2")


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
    return render_template('login.html')

@app.route('/run_login', methods=['GET', 'POST'])
def run_login():

    username = request.form['username']
    password = request.form['password']

    # Grabs the whole table of user from the database
    users = database.Table("User")
    for i in range(users.item_count):
        record = users.get_item(Key={"ID": i})
        # Admin login
        if (username == record['Item']['Username']) and (password == record['Item']['Password']):
            if record['Item']['AccountID']=="Admin":
                login_user(user)
                url = "/admin"

            elif record['Item']['AccountID']=="Student":
                login_user(user)
                url = "/moduleSelection"
            return jsonify({'success': 'success', 'url': url})
    return jsonify({'success': 'success', 'url': '/login'})

@app.route('/profile', methods=['GET', 'POST'])
def profile():
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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    user_form = UserForm()

    return render_template('new-admin.html', title='Account creation')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    # View payload, print request.form or look at html element name
    account_id = request.form['ID']
    dob = request.form['DOB']
    firstname = request.form['FirstName']
    lastname = request.form['LastName']
    # Needs to be a list of strings. [{"S": "Mathematics"}, {"S":  "Science"}, {"S": "English"}]
    modules = request.form['Modules']
    username = request.form['Username']
    password = request.form['Password']

    user_table = database.Table['User']

    user_table.put_item(
        TableName='User',
        Item={
            'AccountID': account_id,
            'DOB': dob,
            'FirstName': firstname,
            'LastName': lastname,
            'Modules': modules,
            'Username': username,
            'Password': password
        }
    )

    return jsonify({'success': 'success'})


@app.route('/moduleSelection', methods=['GET', 'POST'])
def module_selection():
    return render_template('moduleSelection.html', title='Module Selection')


if __name__ == "__main__":
    app.run()
