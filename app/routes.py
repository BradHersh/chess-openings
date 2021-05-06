from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Results
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from flask import jsonify, request
from statistics import mode
import re
from sqlalchemy import func, select, distinct
import numpy as np
import json

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/learn')
@login_required
def learn():
    return render_template('learn.html', title='Learn')

@app.route('/Test')
@login_required
def Test():
    return render_template('Test.html', title='Test')

@app.route('/chesspractice/<opening>/', methods=['GET', 'POST'])
@login_required
def chesspractice(opening):
    name = {'opening': opening}
    return render_template('chesspractice.html', title='Test', name = name)

@app.route('/chesstest/<opening>/', methods=['GET', 'POST'])
@login_required
def chesstest(opening):
    name = {'opening': opening}
    return render_template('chesstest.html', title='Test', name = name)

@app.route('/complete', methods=['GET', 'POST'])
@login_required
def complete():
    score = request.form['score']
    score = score.split('%')[0]
    score = float(score)
    current_opening = request.form['opening']
    wrong = request.form['incorrect']
    if score > 50:
        result = Results(opening=current_opening, result=score, incorrect = wrong, passed = True, student = current_user)
        db.session.add(result)
        db.session.commit()
        flash("well done test complete")
    else:
        result = Results(opening=current_opening, result=score, incorrect = wrong, passed = False, student = current_user)
        db.session.add(result)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    u = User.query.get(current_user.id)
    return render_template('results.html', title='results', query = u.results.all())



@app.route('/feedback/<opening>/', methods=['GET', 'POST'])
@login_required
def feedback(opening):
    lst = []
    lst1 = []
    flatlist = []
    lst2 = []
    lst3 = []
    lst4 = []
    res = Results.query.filter_by(user_id = current_user.id, opening = opening)
    for i in res:
        wrong = i.incorrect
        lst.append(wrong)
    if len(lst) != 0:

        for x in lst:
            lst2.append(x.split(','))
        
        flattened = [val for sublist in lst2 for val in sublist]

        length = len(flattened)
        if length > 3:
            for i in range(1,len(flattened)):
                if i%3 == 0:
                    lst3.append(flattened[i-3:i])
            for i in lst3:
                x = ','.join(i)
                lst4.append(x)
        else:
            for i in range(1,len(flattened)+1):
                if i%3 == 0:
                    lst3.append(flattened[i-3:i])
            for i in lst3:
                x = ','.join(i)
                lst4.append(x)           

        most = mode(lst4)
        most = most.split(',')
        oldPos = most[0]
        mistake = most[1]
        correct = most[2]
        

        return render_template('feedback.html', title='feedback', right = correct, Pos = oldPos, wrong = mistake, opening = opening) 
    else:
        return "Test not attempted yet"


@app.route('/feedback2/', methods=['GET', 'POST'])
def feedback2():
    return render_template('feedback2.html', title='feedback') 

@app.route('/feedback2/<opening>', methods=['GET', 'POST'])
def feedback3(opening):
     res = Results.query.filter_by(user_id = current_user.id, opening = opening)
     lst = []
     i = 1
     for r in res:
         x = r.incorrect
         x = re.findall(",".join(["[^,]+"] * 3), x)

         lst.append(x)
    
    
    
     
     return render_template('feedback3.html', title='feedback3', mistakes = json.dumps(lst), opening = opening)




@app.route('/progress/<opening>/', methods=['GET', 'POST'])
@login_required
def progress(opening):
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    res1 = Results.query.filter_by(user_id = current_user.id, opening = opening)
    openings = []
    marks = []
    time = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = 10
    complete = str((numerator/denominator)*100 ) + '%'
    for r in res1:
        # r.result = r.result.split('%')[0]
        # r.result = float(r.result)
        marks.append(float(r.result))
    tries = list(np.arange(1,len(marks)+1))
    

    return render_template('progress.html', title='progress', prog =complete, grades = marks, attempt = tries, opening = opening)