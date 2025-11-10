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
