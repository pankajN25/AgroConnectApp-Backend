import json
from datetime import datetime
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


class mstLocation(SQLObject):
    strLocationName = StringCol(length=200, default=None)
    intCityId = BigIntCol(default=None)
    strAddress = StringCol(length=500, default=None)
    strLandmark = StringCol(length=200, default=None)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    ynDeleted = BoolCol(default=False)


def GetmstLocation():
    try:
        return list(mstLocation.select(mstLocation.q.ynDeleted == False))
    except Exception as e:
        log_exception(file_name="mstLocation_Repository", function_name="GetmstLocation", payload={}, exc=e)
        return []


def GetmstLocationByCityId(city_id):
    try:
        return list(mstLocation.select(AND(mstLocation.q.intCityId == city_id, mstLocation.q.ynDeleted == False)))
    except Exception as e:
        log_exception(file_name="mstLocation_Repository", function_name="GetmstLocationByCityId", payload={"city_id": city_id}, exc=e)
        return []


def savemstLocation(obj):
    try:
        return mstLocation(
            strLocationName=obj.get("strLocationName"),
            intCityId=obj.get("intCityId"),
            strAddress=obj.get("strAddress"),
            strLandmark=obj.get("strLandmark"),
        )
    except Exception as e:
        log_exception(file_name="mstLocation_Repository", function_name="savemstLocation", payload=obj, exc=e)
        return None


def editmstLocation(obj):
    try:
        jstr = json.dumps(obj)
        data = json.loads(jstr, object_hook=datetime_decoder)
        row = mstLocation.get(data['id'])
        row.strLocationName = data.get('strLocationName', row.strLocationName)
        row.intCityId = data.get('intCityId', row.intCityId)
        row.strAddress = data.get('strAddress', row.strAddress)
        row.strLandmark = data.get('strLandmark', row.strLandmark)
        row.dtDateofModification = datetime.now()
        return row
    except Exception as e:
        log_exception(file_name="mstLocation_Repository", function_name="editmstLocation", payload=obj, exc=e)
        return None


def deletemstLocation(obj):
    try:
        row = mstLocation.get(obj['id'])
        row.ynDeleted = True
        return row
    except Exception as e:
        log_exception(file_name="mstLocation_Repository", function_name="deletemstLocation", payload=obj, exc=e)
        return None


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
mstLocation.createTable(ifNotExists=True)
