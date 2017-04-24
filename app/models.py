# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create Student table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, defualt=False)

    @property
    def password(self):
        ''' Prevent password from being accessed '''
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        ''' Set password to a hashed password '''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        ''' Check if hashed password matches actual password '''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}'.format(self.username)

