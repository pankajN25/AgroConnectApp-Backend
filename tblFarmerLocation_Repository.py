from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblFarmerLocation(SQLObject):

    intFarmerId = BigIntCol(default=None)
    floatLatitude = FloatCol(default=0)
    floatLongitude = FloatCol(default=0)
    nvcharAddress = StringCol(length=200)
    dtUpdatedDatetime = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL FARMER LOCATIONS
# =====================================================
def GettblFarmerLocation():
    try:
        return list(tblFarmerLocation.select(tblFarmerLocation.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_Repository",
            function_name="GettblFarmerLocation",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET FARMER LOCATION COUNT
# =====================================================
def GettblFarmerLocationCount():
    try:
        count = tblFarmerLocation.select(tblFarmerLocation.q.ynDeleted == False).count()
        return {"totalFarmerLocationCount": count}
    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_Repository",
            function_name="GettblFarmerLocationCount",
            payload={},
            exc=e
        )
        return {"totalFarmerLocationCount": 0}


# =====================================================
# GET FARMER LOCATIONS BY FARMER ID
# =====================================================
def GettblFarmerLocationByFarmerId(intFarmerId):
    try:
        row = tblFarmerLocation.select(
            AND(
                tblFarmerLocation.q.intFarmerId == intFarmerId,
                tblFarmerLocation.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_Repository",
            function_name="GettblFarmerLocationByFarmerId",
            payload={"intFarmerId": intFarmerId},
            exc=e
        )


# =====================================================
# GET FARMER LOCATION BY ID
# =====================================================
def GettblFarmerLocationById(locationId):
    try:
        return tblFarmerLocation.get(locationId)
    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_Repository",
            function_name="GettblFarmerLocationById",
            payload={"locationId": locationId},
            exc=e
        )
        return None


# =====================================================
# SAVE FARMER LOCATION
# =====================================================
def savetblFarmerLocation(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblFarmerLocation.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            obj.dtUpdatedDatetime = datetime.now()
            return obj

        return tblFarmerLocation(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblFarmerLocation_Repository",
            function_name="savetblFarmerLocation",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT FARMER LOCATION
# =====================================================
def edittblFarmerLocation(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        location = tblFarmerLocation.get(JsonString['id'])

        location.intFarmerId = JsonString['intFarmerId']
        location.floatLatitude = JsonString['floatLatitude']
        location.floatLongitude = JsonString['floatLongitude']
        location.nvcharAddress = JsonString['nvcharAddress']

        location.dtUpdatedDatetime = datetime.now()

        return location

    except Exception as e:

        log_exception(
            file_name="tblFarmerLocation_Repository",
            function_name="edittblFarmerLocation",
            payload=JsonString1,
            exc=e
        )
        return None

# =====================================================
# DELETE FARMER LOCATION
# =====================================================
def deletetblFarmerLocation(JsonString):
    try:
        location = tblFarmerLocation.get(JsonString['id'])
        location.ynDeleted = True
        return location

    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_Repository",
            function_name="deletetblFarmerLocation",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblFarmerLocation.createTable(ifNotExists=True)
