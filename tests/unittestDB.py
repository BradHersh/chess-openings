import unittest, os, time
from app import app, db
from app.models import User
num = 2
class UserTest(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE URI"]=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.session().autoflush = False
        #db.create_all()
        u1 = User(id=1112,username="aaa2", email='aaa2@email.com', password_hash="aaa2")
        db.session.add(u1)
        #db.session.commit()

    def TearDown(self):
        db.session.query(User).delete()
        db.session.commit()
        db.session.remove()
    
    def test_password(self):
        u = User.query.get(1112)
        self.assertNotEqual(u.password_hash,'case')
        self.assertEqual(u.password_hash,'aaa2')

    def test_username(self):
        u = User.query.get(1112)
        self.assertNotEqual(u.username,'case')
        self.assertEqual(u.username,'aaa2')

    def test_email(self):
        u = User.query.get(1112)
        self.assertNotEqual(u.email,'case')
        self.assertEqual(u.email,'aaa2@email.com')


if __name__ == '__main__':
    unittest.main(verbosity=2)