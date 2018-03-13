import json
from flask import current_app

from app import db
from app.mod_db.models import Show, Performer
from app.mod_db.forms import SingleShowForm
from  helper import clock # decorator clock


class ShowToDisplay:
    def __init__(self, show):
        self.id = show.id
        self.title = show.title
        self.showdate = show.showdate
        self.medium = show.medium
        self.source = show.source
        self.location = show.location
        self.number = show.number
        self.lengthinmin = show.lengthinmin
        self.place = show.place
        try:
            # main performer for display
            performer = show.performer[0]
            self.performername = performer.name
            self.performerfirstname = performer.firstname
        except:
            self.performername = ''
            self.performerfirstname = ''

@clock
def getAllShows():
    list = Show.query.all()
    return list

@clock
def searchPerformersInDb(searchitems):
    queryStarted = False
    found = None
    queryresult = None
    # only equal reults, DVD and excluded DVDR
    itemname = searchitems['name']
    if itemname != '':
        looking_for = '%{0}%'.format(itemname)
        if queryStarted == False:
            queryresult = Performer.query.filter(Performer.name.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Performer.name.like(looking_for))
    itemfname = searchitems['firstname']
    if itemfname != '':
        looking_for = '%{0}%'.format(itemfname)
        if queryStarted == False:
            queryresult = Performer.query.filter(Performer.firstname.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Performer.firstname.like(looking_for))
    if  queryStarted:
        found = queryresult.all()

    return found


@clock
def searchInDb(searchitems):
    ''' extract items from searchitems,
    search for all movies, that fulfils the criteria
    return the list of all results'''
    queryStarted = False
    found = None
    queryresult = None
    # only equal reults, DVD and excluded DVDR, that's why not using like(looking_for)
    itemmedium = searchitems['medium']
    if itemmedium != '':
        looking_for = '%{0}%'.format(itemmedium)
        if queryStarted == False:
            queryresult = Show.query.filter_by(medium=itemmedium)
            queryStarted = True
        else:
            queryresult = queryresult.filter_by(medium=itemmedium)


    itemyear = searchitems['year']
    if itemyear != '':
        looking_for = '%{0}%'.format(itemyear)
        if queryStarted == False:
            queryresult = Show.query.filter(Show.showdate.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.showdate.like(looking_for))

    itemplace = searchitems['place']
    if itemplace != '':
        looking_for = '%{0}%'.format(itemplace)
        if queryStarted == False:
            queryresult = Show.query.filter(Show.place.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.place.like(looking_for))

    itemlocation = searchitems['location']
    if itemlocation != '':
        looking_for = '%{0}%'.format(itemlocation)
        if queryStarted == False:
            queryresult = Show.query.filter(Show.location.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.location.like(looking_for))

    itemtitle = searchitems['title']
    if itemtitle != '':
        looking_for = '%{0}%'.format(itemtitle)
        if queryStarted == False:
            queryresult = Show.query.filter(Show.title.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.title.like(looking_for))

    itemnumber = searchitems['number']
    if itemnumber != '':
        looking_for = '%{0}%'.format(itemnumber)
        if queryStarted == False:
            queryresult = Show.query.filter(Show.number.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Show.number.like(looking_for))

    if  queryStarted:
        found = queryresult.all()

    return found

@clock
def filterShowsWithPerfName(listRawShows, itemperformer):
    ''' function search for shows with performer
    in the show.performers.list'''
    # dictionary disables the double insert of the same show for various perfs,
    # for instance for Jarrett Trio and K.Jarrett as performers
    dictWithPerf = {}
    looking_for = '%{0}%'.format(itemperformer)

    # create the list of performers, can be bigger as one
    perfs = Performer.query.filter(Performer.name.like(looking_for)).all()

    for perf in perfs:
        for show in listRawShows:
            if show.is_included(perf):
                dictWithPerf[show.id] = show

    listWithPerf = list(dictWithPerf.values())
    # the same results with list compr
    # nlist = [value for key, value in dictWithPerf.items()]
    return listWithPerf

@clock
def searchShowsWithPerformers(perfToSearch):

    looking_for = '%{0}%'.format(perfToSearch)

    # create the list of performers, can be bigger as one
    perfs = Performer.query.filter(Performer.name.like(looking_for)).all()

    dictWithPerf = {}

    for perf in perfs:
        shows = perf.shows.all()
        for show in shows:
            #show = Show.query.filter_by(id = showid)
            dictWithPerf[show.id] = show

    listWithPerf = list(dictWithPerf.values())
    return listWithPerf

def delPerfFromAll(performerid):
    performer = Performer.query.filter_by(id=performerid).first()

    # create the list of shows
    shows = Show.query.all()
    showsToEdit = []
    perfid = performer.id
    for show in shows:
        perflist = show.performers
        for perf in perflist:
            if perf.id == perfid:
                showsToEdit.append(show)

    # remove perf from that shows
    for show in showsToEdit:
        show.delete_performer(performer)

    # at the end del the performer obj
    db.session.delete(performer)
    db.session.commit()


@clock
def updateShow(showid, form):
    commitFlag = False

    obj = Show.query.filter_by(id=showid).first()

    oldTitle = obj.title
    newTitle = form.title.data
    if newTitle != oldTitle:
        commitFlag = True
        obj.title = newTitle

    oldLength = obj.lengthinmin
    newLength = form.lenght.data
    if newLength != oldLength:
        commitFlag = True
        obj.lengthinmin = newLength

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

    newNumber = form.number.data
    oldNumber = obj.number
    if newNumber != oldNumber:
        commitFlag = True
        obj.number = newNumber

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
        newperfid = perf.id
        flagPerfAllocated = False
        performers = obj.performer
        for oldPerf in performers:
            oldId = oldPerf.id
            if oldId == newperfid:
                flagPerfAllocated = True

        if flagPerfAllocated == False:
            current_app.logger.info('added performer to show')
            obj.performers.append(perf)
            commitFlag = True

    if commitFlag == True:
        db.session.commit()


def delPerfFromShow(showid, perfnr, externFlag):
    show = Show.query.filter_by(id=showid).first()
    perf = Performer.query.filter_by(id=perfnr).first()
    show.delete_performer(perf)
    if externFlag:
        db.session.commit()


def updateMediumInDb(foundList, inputMedium):
    for show, newMedium in zip(foundList, inputMedium):
        oldMedium = show.medium
        if newMedium != oldMedium:
            show.medium = newMedium

def updatePlaceInDb(foundList, inputPlace):
    for show, newPlace in zip(foundList, inputPlace):
        oldPlace = show.place
        if newPlace != oldPlace:
            show.place = newPlace

def updateLengthInDb(foundList, inputLength):
    for show, newLength in zip(foundList, inputLength):
        oldLength = str(show.lengthinmin)
        if newLength != oldLength:
            show.lengthinmin = newLength


def add_performer(name, firstname):
    newPerf = Performer(name=name,
                        firstname=firstname)
    db.session.add(newPerf)
    db.session.commit()


def addShow(form):
    location = form.location.data
    title = form.title.data
    year = form.year.data
    medium = form.medium.data
    place = form.place.data
    source = form.source.data
    notes = form.notes.data
    number = form.number.data
    lenght = form.lenght.data
    newShow = Show(
        location=location,
        showdate=year,
        title=title,
        source=source,
        medium=medium,
        number=number,
        lengthinmin=lenght,
        place=place,
        notes=notes
    )
    #TODO check and add/update performer
    # check if new performer added
    newName = form.addperformername.data
    if newName != '':
        newFName = form.addperformerfname.data
        # check if performer already exists
        perf = Performer.query.filter_by(name=newName).filter_by(firstname=newFName).first()
        if perf == None:
            perf = Performer(name=newName, firstname=newFName)
        newShow.performers.append(perf)
    db.session.add(newShow)

    db.session.commit()


def deleteShow(showid):
    show = Show.query.filter_by(id=showid).first()
    db.session.delete(show)
    db.session.commit()


def fillTheShowForm(showid, form):
    show = Show.query.filter_by(id=showid).first()
    form.location.data = show.location
    form.year.data = show.showdate
    form.title.data = show.title
    form.medium.data = show.medium
    form.place.data = show.place
    form.source.data = show.source
    form.number.data = show.number
    form.lenght.data = show.lengthinmin
    form.notes.data = show.notes
