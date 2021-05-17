import unittest2, os, time
from app import app, db
from app.models import User

class UserTest(unittest2.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE URI"]=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()


    def TearDown(self):
        db.session.query(User).delete()
        db.session.commit()
        db.session.remove()
    

    def test_username(self):
        u = User.query.filter_by(username='Test123').first()
        self.assertNotEqual(u.username,'case')
        self.assertEqual(u.username,'Test123')

    def test_email(self):
        u = User.query.filter_by(username='Test123').first()
        self.assertNotEqual(u.email,'case')
        self.assertEqual(u.email,'test123@email.com')


if __name__ == '__main__':
    unittest2.main(verbosity=2)