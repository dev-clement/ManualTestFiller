import unittest
from ManualTestFiller import create_app, db
from ManualTestFiller.models import User

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
        response = self.client.post('/user/signout')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Signed out successfully', data['message'])

