from flask import Flask, render_template, url_for, request
import boto3
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
app.config.from_object('config')

if __name__ == '__main__':
    app.run(debug=True)
#
@app.route("/addquiz", methods=['POST', 'GET'])
def add_quiz():
    if request.method == 'POST':
        quizzes_table = database.Table('Quizzes')
        
        quiz_category = request.form['quiz_category']
        quiz_question = request.form['quiz_question']
        quiz_A = request.form['A']
        quiz_B = request.form['B']
        quiz_C = request.form['C']
        quiz_D = request.form['D']
        quiz_answer = request.form['quiz_answer']

        quizzes_table.put_item(
            TableName='Quizzes',
            Item = {
                'quiz_category': quiz_category,
                'quiz_question': quiz_question,
                'A': quiz_A,
                'B': quiz_B,
                'C': quiz_C,
                'D': quiz_D,
                'quiz_answer': quiz_answer
            }
        )
        return {
            "status":"sent"
        }, 200
#
    if request.method == 'GET':
        return render_template('quiz_creation.html')
#
_page = {
    'category_name': None,
    'NextToken': None,
}
@app.route("/quizbycategory", defaults={'category':None}, methods=['POST'])
@app.route("/quizbycategory/<category>")

def get_quiz_by_category(category):
    if request.method == 'GET':
#        
        quizzes_table = database.Table('Quizzes')
        response = quizzes_table.scan
        get_category = quizzes_table.get_query(KeyConditionExpression=Key('quiz_category').eq(category))
        paginator = quizzes_table.get_paginator(
            quizzes_table.get_querry(
                KeyConditionExpression=Key('quiz_category').eq(category), Select='SPECIFIC_ATTRIBUTES', AttributesToGet=[get_category], Limit = 3
            )
        )
        result = [i['Items'] for i in paginator['Items']]
        _page['category_name'] = category
        if 'NextToken' in paginator.keys():
            _page['NextToken'] = paginator['NextToken'][0]
        #print(_vars)
#
        return render_template('quizpage.html', result=result)   
#
    elif request.method == 'POST':
#        
            if 'next' in request.form.keys():
#
                result = [i['data'] for i in paginator['data']]
                if 'before' in paginator.keys():
                    _page['before'] = paginator['before'][0]
                if 'NextToken' in paginator.keys():
                    _page['NextToken'] = paginator['NextToken'][0]
                return render_template('new_quiz.html', result=result)
#
if __name__ == '__main__':
    app.run(debug=True)