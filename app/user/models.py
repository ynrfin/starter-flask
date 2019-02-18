from app.extensions import db

class User(db.Model):
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    fullname = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active():
        '''True, as all users are active'''
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        '''False, as anonymous user is not supported'''
        return False;
