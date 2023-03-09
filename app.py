from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_home():
    title = satisfaction_survey.title
    instructs = satisfaction_survey.instructions
    return render_template('start.html', title = title, instructs = instructs)

@app.route('/questions/<num>')
def show_questions(num):
    if len(responses) >= len(satisfaction_survey.questions):
        return render_template('thankyou.html')
    if num == len(responses):
        idx = int(num)
    else: 
        flash('Invalid question')
        idx = len(responses)
    title = satisfaction_survey.title
    q = satisfaction_survey.questions[idx].question
    c = satisfaction_survey.questions[idx].choices
    return render_template('questions.html', title = title, q = q, c = c, num = idx)

@app.route('/answer', methods=['POST'])
def accept_answer():
    ans = request.form['ans']
    title = satisfaction_survey.title
    responses.append(ans)
    if len(responses) < len(satisfaction_survey.questions):
        return redirect (f'/questions/{len(responses)}')
    else: 
        return render_template('thankyou.html')