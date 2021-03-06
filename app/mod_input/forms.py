from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

from wtforms.validators import DataRequired

# class ManInputForm(FlaskForm):
#     imdbid = StringField('Imdb ID')
#     localname = StringField('Localname')
#     medium = StringField('Medium')
#     submit = SubmitField('Submit')
#
class ManShowInputForm(FlaskForm):
    title = StringField('Title')
    medium = StringField('Medium')
    place = StringField('Place')
    source = StringField('Source')
    ownrating = StringField('MyOwnRating')
    amgrating = StringField('AMGRating')
    submit = SubmitField('Submit')

class CsvInputForm(FlaskForm):
    filename = StringField('CsvFileName', validators=[DataRequired()])
    find = SubmitField('find file')
    submit = SubmitField('Submit')