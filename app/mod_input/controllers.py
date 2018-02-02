from flask import Blueprint, render_template, flash, redirect, url_for
import csv

from config import Config

from app.mod_input.forms import ManShowInputForm, CsvInputForm
import app.mod_db.controllers as dbc

import helper as h

from app import db
from app.mod_db.models import  Performer, Show

# from app.mod_input.forms import ManInputForm, CsvInputForm
# import app.mod_db.controllers as dbc

mod_input = Blueprint('input', __name__, url_prefix='/mod_input')

@mod_input.route('/manshowinput', methods=['GET', 'POST'])
def manshowinput():
    form = ManShowInputForm()
    if form.validate_on_submit():
        # insertManualInput(form)
        return redirect('/index')
    return render_template('mod_input/manshowinput.html',
                           title='Manual Input',
                           form=form)



@mod_input.route('/csvinput', methods=['GET', 'POST'])
def csvinput():
    form = CsvInputForm()
    if form.validate_on_submit():
        flash('File choosen: {}'.format(
            form.filename.data
        ))

        fileName = '/home/jan/project/musicvideo_db/userdata/musicvideo.csv'
        # fileName = '/home/jan/project/movie_db/userdata/input_80.csv'
        readFileAddItemsToDb(fileName)
        # readFileAddItemsToDb(form.filename.data)
        return redirect('/index')
    return render_template('mod_input/csvinput.html',
                           title='CSV Input',
                           form=form)

def readFileAddItemsToDb(fileName):
    '''
    0,1 ""	"Name"
    2 "date"
    3	"Place"
    4	"titel"
    5,6	"Source"	"Medium"
    7,8 "Time"	"Q"
    9	"CDs"
    10	"notes"
    11	"to trade"
    12	"from"
    13	"nr"
    :param fileName:
    :return:
    '''
    with h.ManagedUtfFile(fileName) as f:
        csvReader = csv.reader(f)
        linecount = 0
        data = False
        for row in csvReader:
            if data == False:
                data = True
            else:
                # first = rawrow[0]
                # row = first.split('\t')
                # row = rawrow
                if len(row) > 0:
                    linecount = linecount + 1
                    name = row[1]
                    firstname = row[0]
                    if len(row) > 3:
                        city = row[3]
                    else:
                        city = ''
                    if len(row) > 2:
                        showdate = row[2]
                    else:
                        showdate = ''
                    if len(row) > 4:
                        title = row[4]
                    else:
                        title = ''
                    if len(row) > 5:
                        source = row[5]
                        if source == '':
                            source = '-'
                    else:
                        source = '-'
                    if len(row) > 6:
                        medium = row[6]
                        if medium == '':
                            medium = '-'
                    else:
                        medium = '-'

                    if len(row) > 9:
                        count = row[9]
                        if count == '':
                            count = '-'
                    else:
                        count = '-'

                    if len(row) > 13:
                        number = row[13]

                    # (imdbID, EAN, title, titleorig, titlelocal, medium, nr, source) = \
                    #     row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]

                    print(name, title, medium, count, number)
                    show = Show(title=title, city=city, showdate=showdate,
                                medium=medium, source=source,
                                number = number
                                )

                    # check the name, if performer already in DB
                    pq = Performer.query.filter_by(name=name).filter_by(firstname=firstname).first()
                    if pq == None:
                        perf = Performer(firstname=firstname, name=name)
                    else:
                        perf = pq

                    show.performers.append(perf)

                    db.session.add(show)
        db.session.commit()