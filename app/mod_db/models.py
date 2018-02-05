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
    notes = db.Column(db.Text())

    def __init__(self, location='',  showdate='', title='', publishyear='',
                  medium='', lengthinmin=0, source='', place='', number=''):
        self.location = location
        self.showdate = showdate
        self.title = title
        self.publishyear = publishyear
        self.source = source
        self.medium = medium
        self.lengthinmin = lengthinmin
        self.place = place
        self.number = number


    def __repr__(self):
        return '<Show showdate={} title={} medium={}'.format(self.showdate, self.title, self.medium)
