import unittest
from flask import session
from ManualTestFiller import create_app, db

class TestSignOut(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_logout(self):
        """Simple logout"""
        response = self.client.post('/user/signout')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Signed out successfully', data['message'])
    
    def test_register_signin_and_logout(self):
        """Register, sign in and logout"""
        email = 'john@example.com'
        pwd = 'abc123'
        response = self.client.post(
            '/user/register'
            , json={'email': email, 'password': pwd}
            , content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('User registered successfully', data['message'])

        response = self.client.post(
            '/user/signin'
            , json={'email': email, 'password': pwd}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(f'Welcome back, {email}', data['message'])
        self.assertEqual(data['status_code'], 200)

        with self.client.session_transaction() as sess:
            self.assertIn('user_id', sess)
            user_id = sess['user_id']
            self.assertIsNotNone(user_id)

        

