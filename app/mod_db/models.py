from app import db


# Define a base model for other database tables to inherit
class DbBase(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


shows = db.Table('shows',
     db.Column('performer_id', db.Integer, db.ForeignKey('performer.id'), primary_key=True),
     db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True)
                 )

class Performer(DbBase):
    ''' could be person or group'''
    firstname = db.Column(db.String(64))
    name = db.Column(db.String(64))
    # relations
    shows = db.relationship('Show', secondary=shows, backref='performer', lazy='dynamic')


class Show(DbBase):
    ''' could be film, or concert'''
    performers = db.relationship('Performer', secondary=shows, backref='show', lazy='dynamic')
    location = db.Column(db.String(64))
    showdate = db.Column(db.String(12))
    title = db.Column(db.String(64))
    publishyear = db.Column(db.String(4))
    source = db.Column(db.String(8))
    medium = db.Column(db.String(8))
    lengthinmin = db.Column(db.Integer)
    number = db.Column(db.String(8))
    place = db.Column(db.String(8))


# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
# )

# class Page(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tags = db.relationship('Tag', secondary=tags, lazy='subquery',
#         backref=db.backref('pages', lazy=True))
#
# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)