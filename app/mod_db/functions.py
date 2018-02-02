import json
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template

from app import db
from app.mod_db.models import Show, Performer


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
        if queryStarted == False:
            queryresult = Show.query.filter_by(showdate=itemyear)
            queryStarted = True
        else:
            queryresult = queryresult.filter_by(showdate=itemyear)

    itemplace = searchitems['place']
    looking_for = '%{0}%'.format(itemplace)
    if itemplace != '':
        if queryStarted == False:
            # queryresult = Movie.query.filter_by(place=itemplace)
            queryresult = Show.query.filter(Show.location.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.location.like(looking_for))


    if  queryStarted:
        found = queryresult.all()

    return found

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

# def updateMovie(movieid, form):
#     '''
#     movie without imdbId can get imdbId,
#     rest can get new medium (bought dvd) or user rating
#     :param movieid: db id
#     :param form: UpdateMovieForm to extract input data
#     '''
#     obj = Movie.query.filter_by(id=movieid).first()
#     imdbId = form.imdbid.data
#
#     amgRatingNew = form.ratingAmg.data
#     amg = Critic.query.filter_by(name='AMG').first()
#     updateRating(obj, amg, amgRatingNew)
#
#     ownRatingNew = form.ownrating.data
#     jd = Critic.query.filter_by(name='JD').first()
#     updateRating(obj, jd, ownRatingNew)
#
#     oldTitle = obj.titleLocal
#     newTitle = form.localname.data
#     if newTitle != oldTitle:
#         obj.titleLocal = newTitle
#
#     oldMedium = obj.medium
#     newMedium = form.medium.data
#     if newMedium != oldMedium:
#         obj.medium = newMedium
#
#     newplace = form.place.data
#     oldplace = obj.place
#     if newplace != oldplace:
#         obj.place = newplace
#
#     oldImdb = obj.imdbId
#     if oldImdb == '' or oldImdb == '0000000':
#         if imdbId != '' and imdbId != '0000000':
#             updateMovieWithoutIDWithImdb(obj, imdbId, commit=False)
#     db.session.commit()

# def updateRating(movie, critic, newRating):
#
#     ratingOldObj = getRatingForMovie(movie, critic)
#     if ratingOldObj != None:
#         ownRatingOld = ratingOldObj.value
#     else:
#         ownRatingOld = None
#     if(newRating != ownRatingOld) and (newRating != ''):
#         if(ratingOldObj == None):
#             newRating = Rating(movie_id=movie.id, critic_id=critic.id, value=newRating)
#             db.session.add(newRating)
#         else:
#             ratingOldObj.value = newRating


# def updateCritic(criticid, form):
#     obj = Critic.query.filter_by(id=criticid).first()
#     name = form.name.data
#     url = form.url.data
#     maxVal = form.maxval.data
#     obj.name = name
#     obj.url = url
#     obj.maxVal = maxVal
#     db.session.commit()




def updateMediumInDb(foundList, inputMedium):
    pass

def updatePlaceInDb(foundList, inputMedium):
    for i in range(len(foundList)):
        newPlace = inputMedium[i]
        movie = foundList[i]
        oldPlace = movie.place
        if newPlace != oldPlace:
            movie.place = newPlace