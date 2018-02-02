import json
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template

from app import db
from app.mod_db.models import Performer, Show
from app.mod_db.forms import SearchDbForm, ShowsResultsForm

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

        searchitems = json.dumps(searchdir)
        return redirect(url_for('database.showsresults', searchitems=searchitems))
        # if searchitems['amgrating'] =='':
        #     return redirect(url_for('database.pageresults', searchitems=searchitems))
        # else:
        #     return redirect(url_for('database.amgresults', searchitems=searchitems))

    # show form with proper message
    return render_template('mod_db/search.html',
                            title='Search Show',
                            form=form,
                            message=foundMessage)

@mod_db.route('/showsresults/<searchitems>', methods=['GET', 'POST'])
def showsresults(searchitems):
    form = ShowsResultsForm()
    # we need the results of search onSubmit too,
    # to update the medium and ratings
    searchdir = json.loads(searchitems)
    foundShowsList = searchInDb(searchdir)
    resultCount = len(foundShowsList)

    listShowsToDisplay = foundShowsList
    # if foundShowsList != None:
    #     for movie in foundShowsList:
    #         movieToDisplay = convertMovieToDIsplay(movie)
    #         listMovieToDisplay.append(movieToDisplay)


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
                           shows=foundShowsList
                           )

