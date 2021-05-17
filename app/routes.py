from flask import render_template, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Results, Openings
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from flask import jsonify, request
from statistics import mode
import re
from sqlalchemy import func, select, distinct, desc
import numpy as np
import json


#create the homepage and provide variables for progress bar
@app.route('/')
@app.route('/index')
@login_required
def index():
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)
    num = round((numerator/denominator)*100, 2)

    complete = str(round((numerator/denominator)*100, 2)) + '%'

    return render_template('index.html', title='Home' , prog =complete)

#create login page using login form
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
        if request.form.get("username") == "admin":
            session['logged_in'] = True
            return redirect('/admin')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#create logout route 
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


#create register route using flask register form 
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


#create the route to practice an opening
@app.route('/chesspractice/<opening>/', methods=['GET', 'POST'])
@login_required
def chesspractice(opening):
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'
    #query database to pass though relevant opening FEN and name 
    opening = Openings.query.filter_by(name = opening)
    fen = opening[0].FEN
    opening = opening[0].name
    return render_template('chesspractice.html', title='Test', name = json.dumps(fen), prog=complete, opening = opening)

#create route to test an opening 
@app.route('/chesstest/<opening>/', methods=['GET', 'POST'])
@login_required
def chesstest(opening):
    #query database to pass through relevant FEN and opening name 
    opening = Openings.query.filter_by(name = opening)
    fen = opening[0].FEN
    name = opening[0].name

    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'

    return render_template('chesstest.html', title='Test', opening = json.dumps(fen), name = name, prog = complete)

#when a test is completed, this route commits all relevant details (mistakes, grade, student etc) to the database and redirects to index
@app.route('/complete', methods=['GET', 'POST'])
@login_required
def complete():
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'
    test_results = request.json
    score  = test_results['score']
    score = float(score)
    current_opening = test_results['opening']
    wrong_moves = test_results['wrong']
    wrong_moves = [item for sublist in wrong_moves for item in sublist]
    wrong_moves = ','.join(wrong_moves)
    if score > 50:
        result = Results(opening=current_opening, result=score, incorrect = wrong_moves, passed = True, student = current_user)
        db.session.add(result)
        db.session.commit()
        flash("well done test complete")
    else:
        result = Results(opening=current_opening, result=score, incorrect = wrong_moves, passed = False, student = current_user)
        db.session.add(result)
        db.session.commit()
    return render_template('index.html', title='Home' , prog =complete)


#create route to select which opening to see results for 
@app.route('/selectresult/', methods=['GET', 'POST'])
@login_required
def selectresult():
    openings = Openings.query.all()
    lst = []
    for o in openings:
        lst.append(o.name)
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'
    return render_template('selectresult.html', title='Results', openings = lst, prog=complete) 


#viewing results
@app.route('/results/<opening>/', methods=['GET', 'POST'])
@login_required
def results(opening):
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'
    u = User.query.get(current_user.id)

    res = Results.query.filter_by(user_id = current_user.id, opening = opening)
    return render_template('results.html', title='results', query = res, prog=complete, opening = opening)






#creates route to select opening to view feedback for  
@app.route('/feedback2/', methods=['GET', 'POST'])
@login_required
def feedback2():
    openings = Openings.query.all()
    lst = []
    for o in openings:
        lst.append(o.name)

    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'

    return render_template('feedback2.html', title='feedback', openings = lst, prog=complete) 


#creates route to view feedback 
@app.route('/feedback2/<opening>', methods=['GET', 'POST'])
@login_required
def feedback3(opening):
     res3 = Results.query.filter_by(user_id = current_user.id, opening = opening)
     lst = []
     lst1 = []
     i = 1
     for r in res3:
         x = r.incorrect
         y = r.feedback
         x = re.findall(",".join(["[^,]+"] * 3), x)

         lst.append(x)
         lst1.append(y)

     res = Results.query.filter_by(user_id = current_user.id, passed = True)
     res1 = Results.query.filter_by(user_id = current_user.id, opening = opening)
     openings = []
     marks = []
     time = []
     for r in res:
         openings.append(r.opening)
     numerator = len(set(openings))
     denominator = Openings.query.all()
     denominator = len(denominator)
     complete = str(round((numerator/denominator)*100, 2)) + '%'
     for r in res1:
         # r.result = r.result.split('%')[0]
         # r.result = float(r.result)
         marks.append(float(r.result))
     tries = list(np.arange(1,len(marks)+1))
     
     return render_template('feedback3.html', title='feedback3', mistakes = json.dumps(lst), feedback = json.dumps(lst1), opening = opening, prog =complete, grades = marks, attempt = tries)



#creates route to generate page to select opening to learn 
@app.route('/newLearn', methods=['GET', 'POST'])
@login_required
def newLearn():
    openings = Openings.query.all()
    lst = []
    for o in openings:
        lst.append((o.name, o.FEN))
    
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'
    return render_template('newLearn.html', title='Learn', openings = json.dumps(lst), prog=complete)

#creates route to generate page to select opening to test
@app.route('/newTest', methods=['GET', 'POST'])
@login_required
def newTest():
    openings = Openings.query.all()
    lst = []
    for o in openings:
        lst.append((o.name, o.FEN))

    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'
    return render_template('newTest.html', title='Test', openings = json.dumps(lst), prog=complete)


#create route to see aggregate results for whole website
@app.route('/aggregateresults', methods=['GET', 'POST'])
@login_required
def aggregateresults():
    res = Results.query.filter_by(user_id = current_user.id, passed = True)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = Openings.query.all()
    denominator = len(denominator)

    complete = str(round((numerator/denominator)*100, 2)) + '%'
    lst = []
    numopenings = db.session.query(Openings.name).count()
    numtests = db.session.query(Results.result).count()
    numusers  = db.session.query(User.username).count()-1
    commonopening = db.session.query(Results.opening,
    func.count(Results.opening).label('qty')
    ).group_by(Results.opening
    ).order_by(desc('qty'))[0][0]
    # averagemark = np.array(db.session.query(Results.result))
    averagemark = Results.query.all()
    for r in averagemark:
        lst.append(int(r.result))
    lst = np.array(lst)
    averagemark = str(round(np.average(lst),2)) + '%'
    bestusers = db.session.query(Results.user_id,
    func.count(Results.result).label('qty')
    ).group_by(Results.user_id
    ).order_by(desc('qty'))
    for i in bestusers:
        if i[0]!=None:
            x = i[0]
            bestuser = User.query.get(x).username

            break
        else: 
            x = "not yet"
            bestuser = x





    return render_template('aggregateresults.html', title='Aggregateresults', numopenings = numopenings, numtests = numtests, 
    numusers = numusers, commonopening = commonopening, averagemark = averagemark, bestuser = bestuser, prog=complete) 


