from ManualTestFiller import db

class UserTestLink(db.Model):
    __tablename__ = "user_test_link"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), primary_key=True)
    assigned_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', back_populates='test_links')
    test = db.relationship('Test', back_populates='user_links')
