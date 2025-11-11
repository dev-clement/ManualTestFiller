from ManualTestFiller import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    user_links = db.relationship('UserTestLink', back_populates='test')

    def __repr__(self):
        return "<Test id={self.id}, title={self.title}>"
