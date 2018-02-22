from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, TextAreaField

from wtforms.validators import DataRequired


class SingleShowForm(FlaskForm):
    location = StringField('Location')
    title = StringField('Title')
    year = StringField('Year')
    medium = StringField('Medium')
    place = StringField('Place')
    source = StringField('Source')
    lenght = IntegerField('Length in min')
    notes = TextAreaField('Notes')
    number = StringField('Number')

class SearchDbForm(SingleShowForm):
    performer = StringField('Performer')
    submit = SubmitField('Search')

# class SingleResultForm(SingleMovieForm):
#     submit = SubmitField('Submit')
#
#
class AddShowForm(SingleShowForm):
    addperformername = StringField('Name')
    addperformerfname = StringField('First Name')
    submit = SubmitField('Add')

class DeleteShowForm(SingleShowForm):
    submit = SubmitField('Delete')

class EditShowForm(SingleShowForm):
    addperformername = StringField('Add Performer Name')
    addperformerfname = StringField('Add Performer First Name')
    submit = SubmitField('Update')

class ShowsResultsForm(FlaskForm):
    submit = SubmitField('Update')

class ShowsPerformersForm(FlaskForm):
    addperformername = StringField('Add Performer Name')
    addperformerfname = StringField('Add Performer First Name')
    submit = SubmitField('Update')

class SinglePerformerForm(FlaskForm):
    id = IntegerField('ID')
    firstname = StringField('First Name')
    name = StringField('Name')

class EditPerformerForm(SinglePerformerForm):
    submit = SubmitField('Update')

class AddPerformerForm(SinglePerformerForm):
    submit = SubmitField('Add')

class DeletePerformerForm(SinglePerformerForm):
    submit = SubmitField('Delete')

class DeletePerformerFromShowForm(SinglePerformerForm):
    location = StringField('Location')
    title = StringField('Title')
    year = StringField('Year')
    submit = SubmitField('Delete')

class SearchPerformerForm(SinglePerformerForm):
    submit = SubmitField('Search')

