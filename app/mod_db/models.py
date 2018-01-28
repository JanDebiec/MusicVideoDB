from app import db


# Define a base model for other database tables to inherit
class DbBase(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class Person(DbBase):
    name = db.Column(db.String(64))
    # relations
    shows = db.relationship('Show', backref='performer', lazy='dynamic')


class Show(DbBase):
    name = db.Column(db.String(64))
    place = db.Column(db.String(64))
    showdate = db.Column(db.DateTime)
    publishyear = db.Column(db.String(4))
    medium = db.Column(db.String(8))
    source = db.Column(db.String(8))
    place = db.Column(db.String(8))
    lengthinmin = db.Column(db.Integer)
