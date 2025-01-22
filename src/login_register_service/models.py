from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from hashlib import sha256

db = SQLAlchemy()

class UserAlreadyExistsException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()

    @classmethod
    def add_user(cls, email, password):
        if cls.query.filter_by(email=email).first():
            raise UserAlreadyExistsException("A user with that email already exists.")
        user = cls(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def verify_user(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if not user or user.password != cls.hash_password(password):
            raise InvalidCredentialsException("Invalid credentials.")
        return user
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))