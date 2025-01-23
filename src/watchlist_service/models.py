from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from dataclasses import dataclass

db = SQLAlchemy()

class WatchlistMovieAlreadyExistsException(Exception):
    pass

@dataclass
class WatchlistModel(db.Model):
    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    imdb_id = db.Column(db.String(120), nullable=False)
    added_date = db.Column(db.BigInteger, nullable=False)
    year = db.Column(db.Integer)
    poster = db.Column(db.String(512), nullable=True)

    def __init__(self, user_id, title, type, imdb_id, added_date, year=None, poster=None):
        self.user_id = user_id
        self.title = title
        self.type = type
        self.imdb_id = imdb_id
        self.added_date = added_date
        self.year = year
        self.poster = poster
        
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "type": self.type,
            "imdb_id": self.imdb_id,
            "added_date": self.added_date,
            "year": self.year,
            "poster": self.poster,
        }

    @classmethod
    def add_movie(cls, user_id, title, type, imdb_id, added_date, year=None, poster=None):
        if cls.query.filter_by(user_id=user_id, imdb_id=imdb_id).first():
            raise WatchlistMovieAlreadyExistsException("A movie with that IMDb ID already exists in the watchlist of that user.")
        
        movie = cls(
            user_id=user_id,
            title=title,
            type=type,
            imdb_id=imdb_id,
            added_date=added_date,
            year=year,
            poster=poster,
        )
        
        db.session.add(movie)
        db.session.commit()
        return movie
    
    @classmethod
    def remove_movie(cls, user_id, imdb_id):
        movie = cls.query.filter_by(user_id=user_id, imdb_id=imdb_id).first()
        if movie is None:
            return None
        
        db.session.delete(movie)
        db.session.commit()
        return movie
    
    @classmethod
    def get_movies(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    

class WatchlistMovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    type = fields.Str(required=True)
    imdb_id = fields.Str(required=True)
    added_date = fields.Int(required=True)
    year = fields.Int()
    poster = fields.Str()
    
class WatchlistMovieIdSchema(Schema):
    imdb_id = fields.Str(required=True)