import unittest
from ManualTestFiller import create_app, db
from ManualTestFiller.models import User

class TestUserRegister(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        with self.ctx:
            self.ctx.push()
            db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    def test_register_success(self):
        response = self.client.post(
            '/user/register'
            , json={'email': 'john@example.com', 'password': 'abc123'}
            , content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('User registered successfully', data['message'])

        # Check the user actually exists in DB
        with self.ctx:
            user = User.query.filter_by(email='john@example.com').first()
            self.assertIsNotNone(user)

    def test_register_with_no_password(self):
        """Check what happened if a user register with not all data"""
        response = self.client.post(
            '/user/register'
            , json={'email': 'john@example.com'}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual('password is required', data['error'])

        with self.ctx:
            user = User.query.filter_by(email='john@example.com').first()
            self.assertIsNone(user)

    def test_register_with_no_email(self):
        """Check what happened if a user register with no email"""
        response = self.client.post(
            '/user/register'
            , json={'password': 'example123'}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual('email is required', data['error'])

        with self.ctx:
            user = User.query.filter_by(password='example123').first()
            self.assertIsNone(user)
    
    def test_register_same_email(self):
        """Check what happened when you are trying to register the same email twice"""
        response = self.client.post(
            '/user/register'
            , json={'email': 'test@example.com', 'password': 'abc123'}
            , content_type='application/json'
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', data['message'])
        response_dup = self.client.post(
            '/user/register'
            , json={'email': 'test@example.com', 'password': 'abc123'}
            , content_type='application/json'
        )
        data_dup = response_dup.get_json()
        self.assertEqual(response_dup.status_code, 409)
        self.assertEqual('Email already exists', data_dup['message'])
        self.assertEqual('error', data_dup['status'])
