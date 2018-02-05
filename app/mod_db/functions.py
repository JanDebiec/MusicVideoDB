import json
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template

from app import db
from app.mod_db.models import Show, Performer

class ShowToDisplay:
    def __init__(self,
                 show
                 ):
        self.id = show.id
        self.title = show.title
        self.showdate = show.showdate
        self.medium = show.medium
        self.source = show.source
        self.location = show.location
        self.number = show.number
        self.lengthinmin = show.lengthinmin
        try:
            performer = show.performer[0]
            # mainperformer = Performer.query.filter_by(id=performer).first()
            self.performername = performer.name
            self.performerfirstname = performer.firstname
        except:
            self.performername = ''
            self.performerfirstname = ''

def getAllShows():
    list = Show.query.all()
    return list

def searchInDb(searchitems):
    ''' extract items from searchitems,
    search for all movies, that fulfils the criteria
    return the list of all results'''
    queryStarted = False
    found = None
    queryresult = None
    # only equal reults, DVD and excluded DVDR
    itemmedium = searchitems['medium']
    if itemmedium != '':
        looking_for = '%{0}%'.format(itemmedium)
        if queryStarted == False:
            # for testing:
            # queryresult = Show.query.filter(Show.medium.like(looking_for))
            queryresult = Show.query.filter_by(medium=itemmedium)
            # queryresult = Show.query.filter_by(medium=itemmedium).order_by(Show.year.desc())
            queryStarted = True
        else:
            # queryresult = queryresult.filter(Show.medium.like(looking_for))
            queryresult = queryresult.filter_by(medium=itemmedium)
            # queryresult = queryresult.filter_by(medium=itemmedium).order_by(Movie.year.desc())


    itemyear = searchitems['year']
    if itemyear != '':
        looking_for = '%{0}%'.format(itemyear)
        if queryStarted == False:
            queryresult = Show.query.filter(Show.showdate.like(looking_for))
            # queryresult = Show.query.filter_by(showdate=itemyear)
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.showdate.like(looking_for))
            # queryresult = queryresult.filter_by(showdate=itemyear)

    itemplace = searchitems['place']
    if itemplace != '':
        looking_for = '%{0}%'.format(itemplace)
        if queryStarted == False:
            # queryresult = Movie.query.filter_by(place=itemplace)
            queryresult = Show.query.filter(Show.location.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.location.like(looking_for))

    if  queryStarted:
        found = queryresult.all()

    return found

def filterShowsWithPerfName(listShowsToDisplay, itemperformer):
    listWithPerf = []
    for show in listShowsToDisplay:
        perfName = show.performername
        if itemperformer in perfName:
            listWithPerf.append(show)

    return listWithPerf



#
# def updateMovieManual(movieId, inputTitle, medium, source, place, ownrating):
#
#     found = Movie.query.filter_by(imdbId= movieId).first()
#     found.titleLocal = inputTitle
#     found.medium = medium
#     found.source = source
#     found.place = place
#
#     try:
#         critic = Critic.query.filter_by(name='JD').first()
#         rat = Rating(movie_id=found.id, critic_id=critic.id, value=ownrating)
#         db.session.add(rat)
#     except:
#         pass
#
#
#     db.session.commit()



# def deleteMovie(movieid):
#     obj = Movie.query.filter_by(id=movieid).first()
#     print(obj)
#     db.session.delete(obj)
#     db.session.commit()
def updateShow(showid, form):
    commitFlag = False

    obj = Show.query.filter_by(id=showid).first()

    oldTitle = obj.title
    newTitle = form.title.data
    if newTitle != oldTitle:
        commitFlag = True
        obj.title = newTitle

    newlocation = form.location.data
    oldlocation = obj.location
    if newlocation != oldlocation:
        commitFlag = True
        obj.location = newlocation

    oldyear = obj.showdate
    newyear = form.year.data
    if newyear != oldyear:
        commitFlag = True
        obj.showdate = newyear

    oldMedium = obj.medium
    newMedium = form.medium.data
    if newMedium != oldMedium:
        commitFlag = True
        obj.medium = newMedium

    newplace = form.place.data
    oldplace = obj.place
    if newplace != oldplace:
        commitFlag = True
        obj.place = newplace

    newnotes = form.notes.data
    oldnotes = obj.notes
    if newnotes != oldnotes:
        commitFlag = True
        obj.notes = newnotes

    # check if new performer added
    newName = form.addperformername.data
    if newName != '':
        newFName = form.addperformerfname.data
        # check if performer already exists
        perf = Performer.query.filter_by(name=newName).filter_by(firstname=newFName).first()
        if perf == None:
            perf = Performer(name=newName, firstname=newFName)
        # TODO check if performer already allocated to show
        newperfid = perf.id
        flagPerfAllocated = False
        performers = obj.performer
        for oldPerf in performers:
            oldId = oldPerf.id
            if oldId == newperfid:
                flagPerfAllocated = True

        if flagPerfAllocated == False:
            obj.performers.append(perf)
            commitFlag = True

    if commitFlag == True:
        db.session.commit()


def updateMediumInDb(foundList, inputMedium):
    pass

def updatePlaceInDb(foundList, inputMedium):
    for i in range(len(foundList)):
        newPlace = inputMedium[i]
        movie = foundList[i]
        oldPlace = movie.place
        if newPlace != oldPlace:
            movie.place = newPlace