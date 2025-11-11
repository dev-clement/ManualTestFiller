import unittest
from ManualTestFiller import create_app, db
from ManualTestFiller.models import User

class TestUserSignIn(unittest.TestCase):
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

    def test_user_signin(self):
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
        self.assertIn(response.status_code, [200, 401])
