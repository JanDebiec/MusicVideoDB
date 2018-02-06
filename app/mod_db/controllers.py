import json
import sys
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template
from flask import current_app

from app import db
from app.mod_db.models import Performer, Show
from app.mod_db.forms import DeletePerformerForm, EditPerformerForm, ShowsPerformersForm, SearchPerformerForm, DeletePerformerFromShowForm, SearchDbForm, ShowsResultsForm, EditShowForm

# import app.mod_imdb.controllers as tsv

from app.mod_db.functions import *


mod_db = Blueprint('database', __name__, url_prefix='/mod_db')


@mod_db.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchDbForm()
    foundMessage = 'search'
    # init content of form
    searchdir = {}
    if form.validate_on_submit():
        searchdir['year'] = form.year.data
        searchdir['medium'] = form.medium.data
        searchdir['place'] = form.place.data
        searchdir['performer'] = form.performer.data

        searchitems = json.dumps(searchdir)
        return redirect(url_for('database.showsresults', searchitems=searchitems))

    # show form with proper message
    return render_template('mod_db/search.html',
                            title='Search Show',
                            form=form,
                            message=foundMessage)

@mod_db.route('/searchperformer', methods=['GET', 'POST'])
def searchperformer():
    form = SearchPerformerForm()
    foundMessage = 'search'
    # init content of form
    searchdir = {}
    if form.validate_on_submit():
        searchdir['name'] = form.name.data
        searchdir['firstname'] = form.firstname.data

        searchitems = json.dumps(searchdir)
        return redirect(url_for('database.showperformers', searchitems=searchitems))

    # show form with proper message
    return render_template('mod_db/searchperformer.html',
                            title='Search Performer',
                            form=form,
                            message=foundMessage)


@mod_db.route('/showperformers/<searchitems>', methods=['GET', 'POST'])
def showperformers(searchitems):
    form = ShowsPerformersForm()
    searchdir = json.loads(searchitems)
    foundList = searchPerformersInDb(searchdir)
    foundMessage = 'found {} performers'.format(len(foundList))
    return render_template('mod_db/showperformers.html',
                            title='List Performers',
                            form=form,
                           performers=foundList,
                            message=foundMessage)


@mod_db.route('/editperformer/<performerid>', methods=['GET', 'POST'])
def editperformer(performerid):
    form = EditPerformerForm()
    message = 'Edit Performer'
    if form.validate_on_submit():
        perf = Performer.query.filter_by(id=performerid).first()
        perf.name = form.name.data
        perf.firstname = form.firstname.data
        db.session.commit()
        return redirect(url_for('main.index'))
    perf = Performer.query.filter_by(id=performerid).first()
    form.firstname.data = perf.firstname
    form.name.data = perf.name

    return render_template('mod_db/editperformer.html',
                            title='List Performers',
                            form=form,
                           perf=perf,
                            message=message)

@mod_db.route('/deleteperformer/<performerid>', methods=['GET', 'POST'])
def deleteperformer(performerid):
    form = DeletePerformerForm()
    if form.validate_on_submit():
        delPerfFromAll(performerid)
        return redirect(url_for('index'))
    foundMessage = 'delete Performer from DB and from all Shows?'
    return render_template('mod_db/deleteperformer.html',
                            title='Delete Performer',
                            form=form,
                           perf=perf,
                            message=foundMessage)


@mod_db.route('/edit/<showid>', methods=['GET', 'POST'])
def edit(showid):
    form = EditShowForm()
    foundMessage = 'edit'
    if form.validate_on_submit():
        try:
            updateShow(showid, form)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())

        return redirect(url_for('database.search', message=foundMessage))

    # display the single result
    show = Show.query.filter_by(id=showid).first()
    #
    form.location.data = show.location
    form.title.data = show.title
    form.year.data = show.showdate
    form.medium.data = show.medium
    form.place.data = show.place
    form.source.data = show.source
    form.notes.data = show.notes
    try:
        performers = show.performer
    except:
        current_app.logger.error('performers not found', exc_info=sys.exc_info())


    # show form with proper message
    return render_template('mod_db/edit.html',
                            title='Edit Show',
                            form=form,
                           show=show,
                           performers=performers,
                            message=foundMessage)

@mod_db.route('/deleteperffromshow/<showid>/<perfnr>', methods=['GET', 'POST'])
def deleteperffromshow(showid,perfnr):
    form = DeletePerformerFromShowForm()
    foundMessage = ''

    # print('delete perf nr {} from show id {}'.format(perfnr, showid))
    show = Show.query.filter_by(id=showid).first()
    # nr = int(perfnr)
    if form.validate_on_submit():
        try:
            current_app.logger.info('delete perf nr {} from show id {}'.format(perfnr, showid))
            delPerfFromShow(show, perfnr, True)
            # db.session.commit()
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())

        return redirect(url_for('database.search', message=foundMessage))
    perf = Performer.query.filter_by(id=perfnr).first()
    form.firstname.data = perf.firstname
    form.name.data = perf.name
    form.location.data = show.location
    form.title.data = show.title
    form.year.data = show.showdate
    return render_template('mod_db/deleteperformerfromshow.html',
                           title='Title',
                           message='Delete performer',
                           form=form
                           )




@mod_db.route('/showsresults/<searchitems>', methods=['GET', 'POST'])
def showsresults(searchitems):
    form = ShowsResultsForm()
    searchdir = json.loads(searchitems)
    foundShowsList = searchInDb(searchdir)
    
    # list = 0, if ony show found
    # list = None if search not run

    itemperformer = searchdir['performer']
    if foundShowsList == None:
        if itemperformer != '':
            foundShowsList = getAllShows()
        else:
            resultCount = 0
    else:
        resultCount = len(foundShowsList)

    listShowsToDisplay = []
    if foundShowsList != None:
        for show in foundShowsList:
            showToDisplay = ShowToDisplay(show)
            listShowsToDisplay.append(showToDisplay)

    if itemperformer != '':
        foundList = filterShowsWithPerfName(listShowsToDisplay, itemperformer)
    else:
        foundList = listShowsToDisplay
    resultCount = len(foundList)

    if form.validate_on_submit():
        if request.method == 'POST':
            userinputs = request.form
            newdict = userinputs.to_dict()
            amount = len(newdict)
            # we do not know the amount of ratings or medium
            # we know only global size of input
            flagDbShouldCommit = False
            # extracting user ratings input
            # extracting user medium input
            inputMedium = []
            for i in range(resultCount):
                try:
                    pointerString = 'medium[{}]'.format(i)
                    med = newdict[pointerString]
                    if med != '' and med != '-':
                        flagDbShouldCommit = True
                    inputMedium.append(med)
                except: # no more medium input
                    break
            inputPlace = []
            for i in range(resultCount):
                try:
                    pointerString = 'place[{}]'.format(i)
                    plc = newdict[pointerString]
                    if plc != '' and plc != '-':
                        flagDbShouldCommit = True
                    inputPlace.append(plc)
                except: # no more medium input
                    break

            # updateMediumInDb(foundMovieList, inputMedium)
            # updatePlaceInDb(foundMovieList, inputPlace)
            if flagDbShouldCommit:
                db.session.commit()

        foundMessage = "search once more"
        return redirect(url_for('database.search', message=foundMessage))

    if resultCount == 0:
        foundMessage = 'No movie found, search once more'
        return redirect(url_for('database.search', message=foundMessage))
    return render_template('mod_db/showsresults.html',
                           title='Shows Result',
                           form=form,
                           showscount=resultCount,
                           # ownerRatings = ownerRatings,
                           shows=foundList
                           )

