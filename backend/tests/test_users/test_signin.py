import unittest
from ManualTestFiller import create_app, db
from ManualTestFiller.models import User
from werkzeug.security import generate_password_hash

class TestUserSignIn(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        with self.ctx:
            self.ctx.push()
            db.create_all()
    
    def tearDown(self):
        # Clear the SQLAlchemy session
        db.session.remove()

        # Drop all the table from the database
        db.drop_all()

        try:
            engine = db.engines[self.app]
            engine.dispose()
        except Exception:
            pass # The engine may already been distroyed; we ignore safely then

        # Finally we clear the app context
        self.ctx.pop()

    def test_user_signin_succeed(self):
        email = 'john@example.com'
        user = User(email=email, password=generate_password_hash('hashed_password'))
        db.session.add(user)
        db.session.commit()

        # Try to sign in with hashed password
        response = self.client.post(
            '/user/signin'
            , json={'email': email, 'password': 'hashed_password'}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(f'Welcome back, {email}', data['message'])
        self.assertEqual(data['status_code'], 200)

    def test_user_signin_pwd_fail(self):
        user = User(email='john@example.com', password='hashed_password')
        db.session.add(user)
        db.session.commit()

        # Try to sign in
        response = self.client.post(
            '/user/signin'
            , json={'email': 'john@example.com', 'password': 'hashed_password'}
            , content_type='application/json'
        )
        # Should fail, since password isn't hashed right in this example
        self.assertEqual(response.status_code, 401)
    
    def test_user_invalid_field(self):
        response = self.client.post(
            '/user/signin'
            , json={'toto': 'titi'}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'email is required')
    
    def test_invalid_user(self):
        response = self.client.post(
            '/user/signin'
            , json={'email': 'john@example.com', 'password': generate_password_hash('password')}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Invalid email or password !')
    

    def test_invalid_password(self):
        user = User(email='john@example.com', password=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()

        response = self.client.post(
            '/user/signin'
            , json={'email': 'john@example.com', 'password': 'toto'}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Invalid email or password')
        
