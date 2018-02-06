from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField

from wtforms.validators import DataRequired


class SingleShowForm(FlaskForm):
    location = StringField('Location')
    title = StringField('Title')
    year = StringField('Year')
    medium = StringField('Medium')
    place = StringField('Place')
    source = StringField('Source')
    notes = TextAreaField('Notes')

class SearchDbForm(SingleShowForm):
    performer = StringField('Performer')
    submit = SubmitField('Search')

# class SingleResultForm(SingleMovieForm):
#     submit = SubmitField('Submit')
#
#
class AddShowForm(SingleShowForm):
    submit = SubmitField('Add')

class DeleteShowForm(SingleShowForm):
    submit = SubmitField('Delete')

class EditShowForm(SingleShowForm):
    addperformername = StringField('Add Performer Name')
    addperformerfname = StringField('Add Performer First Name')
    submit = SubmitField('Update')

# class ExploreForm(FlaskForm):
#     localname = StringField('TitleLocal')
#     year = StringField('Year')
#     director = StringField('Director')
#
class ShowsResultsForm(FlaskForm):
    submit = SubmitField('Update')

# class CriticsListForm(FlaskForm):
#     submit = SubmitField('Update')
#
class SinglePerformerForm(FlaskForm):
    firstname = StringField('First Name')
    name = StringField('Name')

class EditPerformerForm(SinglePerformerForm):

    submit = SubmitField('Update')

class DeletePerformerForm(SinglePerformerForm):
    submit = SubmitField('Delete')

class DeletePerformerFromShowForm(SinglePerformerForm):
    location = StringField('Location')
    title = StringField('Title')
    year = StringField('Year')
    submit = SubmitField('Delete')

class SearchPerformerForm(SinglePerformerForm):
    submit = SubmitField('Search')

