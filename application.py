from unittest import case
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
from boto3.dynamodb.conditions import Key

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
increment = database.Table('User').item_count
print(increment)
currentuser = ""


@login.user_loader
def load_user(id):
    return user


@app.route('/')
def home():
    # return redirect('/login')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/run_login', methods=['GET', 'POST'])
def run_login():
    global increment
    global currentuser
    username = request.form['username']
    password = request.form['password']

    # Grabs the whole table of user from the database
    users = database.Table("User")
    for i in range(increment):
        record = users.get_item(Key={"ID": i})
        # Admin login
        if (username == record['Item']['Username']) and (password == record['Item']['Password']):
            currentuser = username
            if record['Item']['AccountID'] == "Admin":
                login_user(user)
                url = "/admin"

            elif record['Item']['AccountID'] == "Student":
                login_user(user)
                url = "/profile"
            elif record['Item']['AccountID'] == "Teacher":
                login_user(user)
                url = "/createquiz"
            return jsonify({'success': 'success', 'url': url})
    return jsonify({'success': 'success', 'url': '/login'})


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if request.method == 'POST':
        user.nickname = request.form['nickname']
        print(user.nickname)
    return render_template('profile.html',
                           title="Profile",
                           form=form,
                           )


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    user_form = UserForm()

    return render_template('new-admin.html', title='Account creation')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    global increment
    # View payload, print request.form or look at html element name
    print(request.form)
    account_id = request.form['ID']
    dob = request.form['DOB']
    firstname = request.form['FirstName']
    lastname = request.form['LastName']
    # don't make account if blank categories
    if (not account_id or not dob or not firstname or not lastname):
        return render_template('new-admin.html', title='Account creation')
    # Welcome to the ugliest code ive ever written
    modules = []
    try:
        modules.append(request.form['Add'])
    except:
        pass
    try:
        modules.append(request.form['Sub'])
    except:
        pass
    try:
        modules.append(request.form['Mul'])
    except:
        pass
    try:
        modules.append(request.form['Div'])
    except:
        pass

    username = request.form['Username']
    password = request.form['Password']

    user_table = database.Table('User')

    user_table.put_item(
        TableName='User',
        Item={
            'ID': increment,
            'AccountID': account_id,
            'DOB': dob,
            'FirstName': firstname,
            'LastName': lastname,
            'Modules': modules,
            'Username': username,
            'Password': password
        }
    )
    increment += 1

    return jsonify({'success': 'success'})


@app.route('/moduleSelection', methods=['GET', 'POST'])
def module_selection():
    return render_template('moduleSelection.html', title='Module Selection')


@app.route('/createquiz', methods=['POST', 'GET'])
def create_quiz():
    return render_template('quiz_creation.html')

@app.route('/addcontent', methods=['POST', 'GET'])
def add_content():
    return render_template('content_creation.html')

@app.route('/additionContent', methods=['POST', 'GET'])
def view_content():
    return render_template('additionContent.html')


@app.route('/addquiz', methods=['POST', 'GET'])
def add_quiz():
    quiz_category = request.form['quiz_category']
    quiz_difficulty = request.form['quiz_difficulty']
    quiz_question = request.form['quiz_question']
    quiz_A = request.form['A']
    quiz_B = request.form['B']
    quiz_C = request.form['C']
    quiz_D = request.form['D']
    quiz_answer = request.form['quiz_answer']

    try:
        modules = database.Table('Module')
        category = modules.get_item(Key={"ModuleID": quiz_category})
        length = len(category['Item']['Questions'])

        currentquestions = category['Item']['Questions']
        currentquestions.append({
            'quiz_question': quiz_question,
            'quiz_difficulty': quiz_difficulty,
            'A': quiz_A,
            'B': quiz_B,
            'C': quiz_C,
            'D': quiz_D,
            'quiz_answer': quiz_answer
        })
        modules.put_item(
            TableName='Module',
            Item={
                'ModuleID': quiz_category,
                'Questions': currentquestions
            }
        )
        # else:
        #     currentquestions = category['Item']['Questions']
        #     currentquestions.append({'quiz_question': quiz_question, 'quiz_difficulty': quiz_difficulty, 'A': quiz_A,
        #                              'B': quiz_B, 'C': quiz_C, 'D': quiz_D, 'quiz_answer': quiz_answer})
        #     modules.put_item(
        #         TableName='Module',
        #         Item={
        #             'ModuleID': quiz_category,
        #             'Questions': currentquestions
        #         }
        #     )
    except:
        print("Adding the question to the database has failed.")

    #
    return jsonify({'success': 'success'})


#

# Helper function to get questionset for a module
def get_questions(module):
    # modules: Addition, Division, Multiplication, Subtraction
    try:
        modules = database.Table("Module")
        modules = modules.get_item(Key={"ModuleID": module})
        questionset = modules['Item']['Questions']
        return questionset
    except:
        print("Database Error")


@app.route('/tempgame/<module>')
def tempgame(module):
    questions = get_questions(module)
    print(questions)
    datatojs = {'questionset': questions, 'numofq': len(questions), 'qmodule': module}
    return render_template('tempgame.html', datajs=datatojs)


@app.route('/addition', methods=['GET', 'POST'])
def gameAddition():
    return render_template('additionGame.html')


@app.route('/addition_questions', methods=['GET'])
def addition_questions():
    module = "Addition"
    questions = get_questions("Addition")
    print(questions)

    question = questions[1]['quiz_question']

    a = questions[1]['A']
    b = questions[1]['B']
    c = questions[1]['C']
    d = questions[1]['D']

    answer = questions[1]['quiz_answer']

    question_data = {'questionset': questions, 'numofq': len(questions), 'qmodule': module}

    return question_data


@app.route('/send_results', methods=['POST', 'GET'])
def send_results():
    # global currentuser
    data = request.form['Score']
    module = request.form['Module']
    numofq = request.form['Num']
    try:
        res = database.Table('Results')
        user = res.get_item(Key={"Username": currentuser})
        modulesdata = user['Item']['Scores']
        modulesdata.append(data)
        res.put_item(
            TableName='Results',
            Item={
                'Username': currentuser,
                'Scores': modulesdata
            }
        )
    except:
        pass
    return jsonify({'success': 'success'})


# WORK IN PROGRESS
# _page = {
#     'category_name': None,
#     'NextToken': None,
# }
# @app.route('/quizbycategory', defaults={'category':None}, methods=['POST'])
# @app.route('/quizbycategory/<category>')
# #
# def get_quiz_by_category(category):
#     if request.method == 'GET':
# #        
#         quizzes_table = database.Table('Quizzes')
#         response = quizzes_table.scan
#         get_category = quizzes_table.get_query(KeyConditionExpression=Key('quiz_category').eq(category))
#         paginator = quizzes_table.get_paginator(
#             quizzes_table.get_querry(
#                 KeyConditionExpression=Key('quiz_category').eq(category), Select='SPECIFIC_ATTRIBUTES', AttributesToGet=[get_category], Limit = 3
#             )
#         )
#         result = [i['Items'] for i in paginator['Items']]
#         _page['category_name'] = category
#         if 'NextToken' in paginator.keys():
#             _page['NextToken'] = paginator['NextToken'][0]
#         #print(_vars)
# #
#         return render_template('quizpage.html', result=result)   
# #
#     elif request.method == 'POST':
# #        
#             if 'next' in request.form.keys():
# #
#                 result = [i['data'] for i in paginator['data']]
#                 if 'before' in paginator.keys():
#                     _page['before'] = paginator['before'][0]
#                 if 'NextToken' in paginator.keys():
#                     _page['NextToken'] = paginator['NextToken'][0]
#                 return render_template('new_quiz.html', result=result)
# #


if __name__ == "__main__":
    app.run()
