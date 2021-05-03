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
def learn():
    return render_template('learn.html', title='Learn')

@app.route('/Test')
def Test():
    return render_template('Test.html', title='Test')

@app.route('/chesspractice/<opening>/', methods=['GET', 'POST'])
def chesspractice(opening):
    name = {'opening': opening}
    return render_template('chesspractice.html', title='Test', name = name)

@app.route('/chesstest/<opening>/', methods=['GET', 'POST'])
def chesstest(opening):
    name = {'opening': opening}
    return render_template('chesstest.html', title='Test', name = name)

@app.route('/complete', methods=['GET', 'POST'])
def complete():
    score = request.form['score']
    score = score.split('%')[0]
    score = float(score)
    current_opening = request.form['opening']
    wrong = request.form['incorrect']
    if score > 50:
        result = Results(opening=current_opening, result=score, incorrect = wrong, student = current_user)
        db.session.add(result)
        db.session.commit()
        flash("well done test complete")
    return redirect(url_for('index'))

@app.route('/results', methods=['GET', 'POST'])
def results():
    u = User.query.get(current_user.id)
    return render_template('results.html', title='results', query = u.results.all())



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    u = User.query.get(current_user.id)
    results = Results.query.all()
    lst = []
    lst1 = []
    flatlist = []
    res = Results.query.filter_by(user_id = current_user.id)
    for i in res:
        wrong = i.incorrect
        lst.append(wrong)
    for i in lst:
        i = re.sub('(,[^,]*),', r'\1 ', i).split()
        lst1.append(i)
    flattened = [val for sublist in lst1 for val in sublist]
    most_wrong = mode(flattened)
    most_wrong = most_wrong.split(',')
    oldPos = most_wrong[0]
    mistake = most_wrong[1]

    return render_template('feedback.html', title='feedback', pos = oldPos, wrong = mistake)



@app.route('/progress', methods=['GET', 'POST'])
def progress():
    res = Results.query.filter_by(user_id = current_user.id)
    openings = []
    for r in res:
        openings.append(r.opening)
    numerator = len(set(openings))
    denominator = 10
    complete = str((numerator/denominator)*100 ) + '%'

    return render_template('progress.html', title='progress', prog =complete)