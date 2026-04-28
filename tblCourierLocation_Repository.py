from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblCourierLocation(SQLObject):

    intOrderId = BigIntCol(default=None)
    floatLatitude = FloatCol(default=0)
    floatLongitude = FloatCol(default=0)
    dtUpdatedDatetime = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL COURIER LOCATIONS
# =====================================================
def GettblCourierLocation():
    try:
        return list(tblCourierLocation.select(tblCourierLocation.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="GettblCourierLocation",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET COURIER LOCATION COUNT
# =====================================================
def GettblCourierLocationCount():
    try:
        count = tblCourierLocation.select(tblCourierLocation.q.ynDeleted == False).count()
        return {"totalCourierLocationCount": count}
    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="GettblCourierLocationCount",
            payload={},
            exc=e
        )
        return {"totalCourierLocationCount": 0}


# =====================================================
# GET COURIER LOCATIONS BY ORDER ID
# =====================================================
def GettblCourierLocationByOrderId(intOrderId):
    try:
        row = tblCourierLocation.select(
            AND(
                tblCourierLocation.q.intOrderId == intOrderId,
                tblCourierLocation.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="GettblCourierLocationByOrderId",
            payload={"intOrderId": intOrderId},
            exc=e
        )


# =====================================================
# GET COURIER LOCATION BY ID
# =====================================================
def GettblCourierLocationById(locationId):
    try:
        return tblCourierLocation.get(locationId)
    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="GettblCourierLocationById",
            payload={"locationId": locationId},
            exc=e
        )
        return None


# =====================================================
# SAVE COURIER LOCATION
# =====================================================
def savetblCourierLocation(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblCourierLocation.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            obj.dtUpdatedDatetime = datetime.now()
            return obj

        return tblCourierLocation(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="savetblCourierLocation",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT COURIER LOCATION
# =====================================================
def edittblCourierLocation(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        location = tblCourierLocation.get(JsonString['id'])

        location.intOrderId = JsonString['intOrderId']
        location.floatLatitude = JsonString['floatLatitude']
        location.floatLongitude = JsonString['floatLongitude']

        location.dtUpdatedDatetime = datetime.now()

        return location

    except Exception as e:

        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="edittblCourierLocation",
            payload=JsonString1,
            exc=e
        )
        return None

# =====================================================
# DELETE COURIER LOCATION
# =====================================================
def deletetblCourierLocation(JsonString):
    try:
        location = tblCourierLocation.get(JsonString['id'])
        location.ynDeleted = True
        return location

    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="deletetblCourierLocation",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblCourierLocation.createTable(ifNotExists=True)
