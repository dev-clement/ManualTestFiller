from ManualTestFiller import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    test_links = db.relationship('UserTestLink', back_populates='user')

    def __repr__(self):
        return "<User id={self.id}, email={self.email}>"