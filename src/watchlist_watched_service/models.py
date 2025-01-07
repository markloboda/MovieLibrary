from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4))
    imdb_id = db.Column(db.String(20), unique=True, nullable=False)
    poster = db.Column(db.String(255))

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    year = fields.Str()
    imdb_id = fields.Str(required=True)
    poster = fields.Str()

class WatchlistEntry(db.Model):
    __tablename__ = 'watchlist_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('watchlist_entries', lazy=True))

class WatchlistEntrySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    movie_id = fields.Int(required=True)
    movie = fields.Nested(MovieSchema, dump_only=True)

class WatchedEntry(db.Model):
    __tablename__ = 'watched_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('watched_entries', lazy=True))

class WatchedEntrySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    movie_id = fields.Int(required=True)
    movie = fields.Nested(MovieSchema, dump_only=True)