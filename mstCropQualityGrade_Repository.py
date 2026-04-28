import json
from datetime import datetime
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


class mstCropQualityGrade(SQLObject):
    strGradeName = StringCol(length=200, default=None)
    strDescription = StringCol(length=500, default=None)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    ynDeleted = BoolCol(default=False)


def GetmstCropQualityGrade():
    try:
        return list(mstCropQualityGrade.select(mstCropQualityGrade.q.ynDeleted == False))
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_Repository", function_name="GetmstCropQualityGrade", payload={}, exc=e)
        return []


def savemstCropQualityGrade(obj):
    try:
        return mstCropQualityGrade(
            strGradeName=obj.get("strGradeName"),
            strDescription=obj.get("strDescription"),
        )
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_Repository", function_name="savemstCropQualityGrade", payload=obj, exc=e)
        return None


def editmstCropQualityGrade(obj):
    try:
        jstr = json.dumps(obj)
        data = json.loads(jstr, object_hook=datetime_decoder)
        row = mstCropQualityGrade.get(data['id'])
        row.strGradeName = data.get('strGradeName', row.strGradeName)
        row.strDescription = data.get('strDescription', row.strDescription)
        row.dtDateofModification = datetime.now()
        return row
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_Repository", function_name="editmstCropQualityGrade", payload=obj, exc=e)
        return None


def deletemstCropQualityGrade(obj):
    try:
        row = mstCropQualityGrade.get(obj['id'])
        row.ynDeleted = True
        return row
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_Repository", function_name="deletemstCropQualityGrade", payload=obj, exc=e)
        return None


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
mstCropQualityGrade.createTable(ifNotExists=True)
