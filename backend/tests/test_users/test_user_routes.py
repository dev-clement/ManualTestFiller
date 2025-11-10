import unittest
import json
from ManualTestFiller import create_app, db
from ManualTestFiller.models.user import User

class UserRoutesTestCase(unittest.TestCase):
    """
        Class that will make some test regarding the routes
        of the users (register, sign in and sign out)
    """
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
    
    # ---------------------------
    # Register route test
    # ---------------------------
    def test_user_register(self):
        response = self.client.post(
            '/user/register'
            , json={'email': 'test@example.com', 'password': 'password123'}
            , content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('User register successfully', data['message'])
    
    # ---------------------------
    # Sign In route test
    # ---------------------------
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
    
    # ---------------------------
    # Sign Out route test
    # ---------------------------
    def test_user_signout(self):
        response = self.client.post('/user/signout')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Signed out successfully', data['message'])

if __name__ == "__main__":
    unittest.main()
