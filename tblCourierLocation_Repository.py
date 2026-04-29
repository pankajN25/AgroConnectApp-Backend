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
# UPSERT COURIER LOCATION BY ORDER ID
# Creates a new record if none exists for the order; updates the latest one.
# =====================================================
def UpsertCourierLocationByOrderId(intOrderId, floatLatitude, floatLongitude):
    try:
        existing = list(tblCourierLocation.select(
            AND(
                tblCourierLocation.q.intOrderId == intOrderId,
                tblCourierLocation.q.ynDeleted == False
            )
        ))
        if existing:
            loc = existing[0]
            loc.floatLatitude = floatLatitude
            loc.floatLongitude = floatLongitude
            loc.dtUpdatedDatetime = datetime.now()
            return loc
        return tblCourierLocation(
            intOrderId=intOrderId,
            floatLatitude=floatLatitude,
            floatLongitude=floatLongitude,
        )
    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="UpsertCourierLocationByOrderId",
            payload={"intOrderId": intOrderId},
            exc=e
        )
        return None


# =====================================================
# GET LATEST COURIER LOCATION BY ORDER ID
# Returns only the single most-recent record.
# =====================================================
def GetLatestCourierLocationByOrderId(intOrderId):
    try:
        rows = list(tblCourierLocation.select(
            AND(
                tblCourierLocation.q.intOrderId == intOrderId,
                tblCourierLocation.q.ynDeleted == False
            )
        ))
        if not rows:
            return None
        return max(rows, key=lambda x: x.dtUpdatedDatetime or datetime.min)
    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_Repository",
            function_name="GetLatestCourierLocationByOrderId",
            payload={"intOrderId": intOrderId},
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblCourierLocation.createTable(ifNotExists=True)
