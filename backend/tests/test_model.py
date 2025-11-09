import unittest
from ManualTestFiller import create_app, db
from ManualTestFiller.models.user import User
from ManualTestFiller.models.tests import Test
from ManualTestFiller.models.user_test_link import UserTestLink
from sqlalchemy.exc import IntegrityError

class ManualTestCase(unittest.TestCase):
    """Base test case for the ManualTestFiller backend"""

    def setUp(self):
        """Create a new app context, and a database for each test !"""
        self.app = create_app()
        self.app.config.from_object('ManualTestFiller.config.TestConfig')

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Tear down the database after each test"""
        db.session.remove()
    
    def test_user_creation(self):
        """Test that a user can be created and queried"""
        user = User(email='test@example.com', password='12345')
        db.session.add(user)
        db.session.commit()

        fetched = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.email, 'test@example.com')
        self.assertEqual(fetched.password, '12345')

    def test_user_test_link_relationship(self):
        """Check the user <-> Test many to many relationship"""
        user = User(email='alice@example.com', password='12345')
        test = Test(title='Login functionality')
        link = UserTestLink(user=user, test=test)

        db.session.add_all([user, test, link])
        db.session.commit()

        # Ensure relationship are established correctly
        self.assertEqual(len(user.test_links), 1)
        self.assertEqual(user.test_links[0].test.title, 'Login functionality')
        self.assertEqual(len(test.user_links), 1)
        self.assertEqual(test.user_links[0].user.email, 'alice@example.com')
    
    def test_duplicate_user_email(self):
        """Ensure unique constraint to user.email"""
        user1 = User(email='bob@example.com', password='12345')
        user2 = User(email='bob@example.com', password='12345')
        db.session.add_all([user1, user2])

        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback() # Important: Clean up the session after exception !

if __name__ == "__main__":
    unittest.main()
