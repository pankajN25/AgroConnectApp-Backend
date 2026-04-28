import json
from datetime import datetime
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


class mstCropCategory(SQLObject):
    strCategoryName = StringCol(length=200, default=None)
    strDescription = StringCol(length=500, default=None)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    ynDeleted = BoolCol(default=False)


def GetmstCropCategory():
    try:
        return list(mstCropCategory.select(mstCropCategory.q.ynDeleted == False))
    except Exception as e:
        log_exception(file_name="mstCropCategory_Repository", function_name="GetmstCropCategory", payload={}, exc=e)
        return []


def savemstCropCategory(obj):
    try:
        return mstCropCategory(
            strCategoryName=obj.get("strCategoryName"),
            strDescription=obj.get("strDescription"),
        )
    except Exception as e:
        log_exception(file_name="mstCropCategory_Repository", function_name="savemstCropCategory", payload=obj, exc=e)
        return None


def editmstCropCategory(obj):
    try:
        jstr = json.dumps(obj)
        data = json.loads(jstr, object_hook=datetime_decoder)
        row = mstCropCategory.get(data['id'])
        row.strCategoryName = data.get('strCategoryName', row.strCategoryName)
        row.strDescription = data.get('strDescription', row.strDescription)
        row.dtDateofModification = datetime.now()
        return row
    except Exception as e:
        log_exception(file_name="mstCropCategory_Repository", function_name="editmstCropCategory", payload=obj, exc=e)
        return None


def deletemstCropCategory(obj):
    try:
        row = mstCropCategory.get(obj['id'])
        row.ynDeleted = True
        return row
    except Exception as e:
        log_exception(file_name="mstCropCategory_Repository", function_name="deletemstCropCategory", payload=obj, exc=e)
        return None


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
mstCropCategory.createTable(ifNotExists=True)
