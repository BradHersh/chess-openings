from datetime import datetime

from sqlalchemy.sql.sqltypes import NullType
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, admin 
from sqlalchemy.types import PickleType, ARRAY
from flask_admin.contrib.sqla import ModelView
from flask import session, abort
from flask_admin.menu import MenuLink

#create the SQL user table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    results = db.relationship('Results', backref = 'student', lazy = 'dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

#create the SQL results table
class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opening = db.Column(db.String(140))
    result =db.Column(db.Integer)
    incorrect = db.Column(db.ARRAY(db.String(140)))
    passed = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    feedback = db.Column(db.Text, default = None)




#create the SQL openings table
class Openings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    FEN = db.Column(db.String(1000))


    

    def __repr__(self):
        return '<Results {}>'.format(self.result)



    def __repr__(self):
        return '<Post {}>'.format(self.body)


#create Flask-Admin views - the user interface to access the database
class SecureModelView(ModelView):
    
    def is_accessible(self):
        if "logged_in" in session:
                return True
        else:
            abort(403)

class ResultsView(SecureModelView):
    column_list = ('opening', 'result', 'student', 'passed', 'timestamp', 'feedback')
    form_columns = ('feedback', 'result', 'passed')



@login.user_loader
def load_user(id):
    return User.query.get(int(id))





admin.add_view(SecureModelView(Openings, db.session))
admin.add_view(SecureModelView(User, db.session))
admin.add_view(ResultsView(Results, db.session))
admin.add_link(MenuLink(name='Logout', category='', url='/logout'))