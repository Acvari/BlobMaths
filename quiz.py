import os
from flask import Flask, session, render_template, url_for, redirect, request, flash
import boto3
import json

#
#from copy import deepcopy
# was going to use deepcopy to not alter the dictionary, will do later
#
from datetime import datetime, date, time
from random import choice, shuffle
#
# Create Flask app with random generated key per session
app = Flask(__name__)
app.secret_key = os.urandom(24)
# Currently storing the placeholder questions in a dictionary
questions = {
    '1': {'tip': 'It rhymes with home', 'answer': 'Rome', 'question': 'What is the capital of Italy?', 'options': ['Bruxelles', 'Bucharest', 'Rome', 'Prague']},
    '2': {'tip': 'DingDong2', 'answer': 'Paris', 'question': 'What is the capital of France?', 'options': ['London', 'Paris', 'Berlin', 'Moscow']},
    '3': {'tip': 'DingDong3', 'answer': 'Berlin', 'question': 'What is the capital of Germany?', 'options': ['Berlin', 'Paris', 'Bucharest', 'Kiev']},
    '4': {'tip': 'DingDong4', 'answer': 'Madrid', 'question': 'What is the capital of Spain', 'options': ['Stockholm', 'Madrid', 'Vienna', 'Berlin']},
}
# Variables for storing/tracking the Right/Wrong answers and Current Question
q_tracking={}
q_tracking["correct"]=[]
q_tracking["wrong"]=[]
q_tracking["currentq"]=1
#
app.nquestions=len(questions) # used for the HTML template to display the total number of questions

#SET THE APP ROUTE FOR THE QUIZ TO /MQQuiz (Stands for MULTIPLE QUESTION QUIZ)

@app.route('/MQQuiz', methods=['GET', 'POST'])
def start():
#	
  if request.method == "POST":
    
    # The data has been submitted via POST request.
    #
    entered_answer = request.form.get('quiz_answer', '')
#   
    if not entered_answer:
      flash("Please choose an answer", "error") # Show error if no answer entered
    
    else:

      current_answer=request.form['quiz_answer']
      correct_answer=questions[session["current_question"]]["answer"]
# 
      if current_answer == correct_answer[:len(current_answer)]: 
        q_tracking["correct"].append(int(session["current_question"]))
#      
      else:
        q_tracking["wrong"].append(int(session["current_question"]))
#		
      if current_answer == correct_answer[:len(current_answer)]:
        session["current_question"] = str(int(session["current_question"])+1)
        q_tracking["currentq"]= max(int(session["current_question"]), q_tracking["currentq"])	  
#   
      if session["current_question"] in questions:
        # If the question exists in the dictionary, redirect to the question
        #
        redirect(url_for('start'))
      
      else:
        # else redirect to the summary template as the quiz is complete.
        q_tracking["wrong"]=list(set(q_tracking["wrong"]))
        q_tracking["correct"]=list(set(q_tracking["correct"]))		
        return render_template("quiz_end.html",summary=q_tracking)
#  
  if "current_question" not in session:
    # Sets the current question to question 1 once the user first loads the page
    session["current_question"] = "1"
#  
  elif session["current_question"] not in questions:
    # If the current question number is not available in the questions
    # dictionary, it means that the user has completed the quiz.
    # This means we can show the result page.
    q_tracking["wrong"]=list(set(q_tracking["wrong"]))
    q_tracking["correct"]=list(set(q_tracking["correct"]))	
    return render_template("quiz_end.html",summary=q_tracking)
  
  # If the request is a GET request 
  currentN = int(session["current_question"])   
  currentQ =  questions[session["current_question"]]["question"]
  a1, a2, a3, a4 = questions[session["current_question"]]["options"] 
  # 
  return render_template('quiz_start.html',num=currentN,ntot=app.nquestions,question=currentQ,ans1=a1,ans2=a2,ans3=a3,ans4=a4)   
#
@app.route('/checkform_quiz',methods=['GET','POST'])
def check_button():
    the_color1='Black';the_color2='Black';the_color3='Black';	
    the_color4='Black';the_color6='Black';
    the_check1='';the_check2='';the_check3='';the_check4='';
#
    if "current_question" not in session:
        session["current_question"] = "1"		
#	
    currentN = int(session["current_question"])   
    currentQ = questions[session["current_question"]]["question"]
    a1, a2, a3, a4 = questions[session["current_question"]]["options"] 
#
    current_answer=request.form['quiz_answer']
    correct_answer=questions[session["current_question"]]["answer"]
    tip=questions[session["current_question"]]["tip"]
#
# tracking the check history might help with analytics later
#
    f = open('mini_log.txt','a') #a is for append
    f.write('%s\n'%(datetime.now().strftime("%A, %d. %B %Y %I:%M%p")))		
    f.write('Current number: %s, '%(currentN))			
    f.write('Current question: %s\n'%(currentQ))	
    f.write('Correct answer: %s\n'%(correct_answer))
    f.write('Current selection: %s\n'%(current_answer))	#	
    f.close()
#
# Checks the answer selected against the correct answer in the dictionary
    if current_answer == correct_answer[:len(current_answer)]: the_color6="Green"
    if current_answer in a1[:len(current_answer)]:
        if current_answer in correct_answer[:len(current_answer)]:
            the_color1="Green"
            the_check1=' - correct'
        else: 
            the_color1="Red"		
            the_check1=' - incorrect'		
#
    if current_answer in a2[:len(current_answer)]:
        if current_answer in correct_answer[:len(current_answer)]:
            the_color2="Green"
            the_check2='- correct'
        else: 
            the_color2="Red"			
            the_check2=' - incorrect'
#
    if current_answer in a3[:len(current_answer)]:
        if current_answer in correct_answer[:len(current_answer)]:
            the_color3="Green"
            the_check3=' - correct'
        else: 
            the_color3="Red"			
            the_check3=' - incorrect'
#			
    if current_answer in a4[:len(current_answer)]:
        if current_answer in correct_answer[:len(current_answer)]:
            the_color4="Green"
            the_check4=' - correct'
        else: 
            the_color4="Red"			
            the_check4=' - incorrect'
#
#		
    return render_template('quiz_answer.html',num=currentN,ntot=app.nquestions,descript=tip,anscheck1=the_check1,anscheck2=the_check2,anscheck3=the_check3,anscheck4=the_check4,ans_color1=the_color1,ans_color2=the_color2,ans_color3=the_color3,ans_color4=the_color4,ans_color6=the_color6,question=currentQ,ans1=a1,ans2=a2,ans3=a3,ans4=a4)
# Runs the app using the web server on port 80, the standard HTTP port
if __name__ == '__main__':
	app.run( 
        # host="0.0.0.0",
        # port=33507

  )