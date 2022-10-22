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
    return redirect('/admin')


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
        # Grabs the whole table of user from the database
        users = database.Table("User")
        record = users.get_item(Key={"ID": 0})
        # In record there is {'Item': {'AccountID': 'Student', ...}} where 'Item' contains all data
        print(record)
        # So go into 'Item'
        print(record['Item'])
        # And pull specific record data
        print(record['Item']['Username'])

        # Admin login
        if (form.username.data == record['Item']['Username']) and (form.password.data == record['Item']['Password']):
            login_user(user)
            return redirect('/admin')
        elif (form.username.data != 'Batting Chestum') and (form.password.data != 'bigload420'):
            flash(f'Incorrect login requested for user {form.username.data}.')
            return redirect('/login')
        login_user(user)
        return redirect('/game')
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


if __name__ == "__main__":
    app.run()
