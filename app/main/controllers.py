from flask import Blueprint, render_template, flash, redirect, url_for

from app.mod_db.models import Performer, Show

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET', 'POST'])
@mod_main.route('/index', methods=['GET', 'POST'])
def index():
    shows = Show.query.all()
    amountShows = len(shows)
    perfs = Performer.query.all()
    amountPerfs = len(perfs)
    messageText = 'MusicVideoDB with {} shows, {} performers'.format(amountShows, amountPerfs)

    return render_template('index.html',
                           message=messageText,
                           title='Home')

