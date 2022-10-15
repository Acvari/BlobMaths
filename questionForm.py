from flask_wtf import FlaskForm
from wtforms import RadioField, FieldList
from wtforms.validators import DataRequired

class answerForm(FlaskForm):
    questions = "What is 1+1?"
    answers = "2"
    answer = RadioField('Label', choices=[(2,'2'),(3,'3'),(4,'4'),(5,'5')])