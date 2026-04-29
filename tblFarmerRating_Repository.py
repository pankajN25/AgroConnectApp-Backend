from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblFarmerRating(SQLObject):

    intFarmerId = BigIntCol(default=None)
    intUserId = BigIntCol(default=None)
    floatRating = FloatCol(default=0)
    nvcharReview = StringCol(length=500)
    dtCreatedDatetime = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL FARMER RATINGS
# =====================================================
def GettblFarmerRating():
    try:
        return list(tblFarmerRating.select(tblFarmerRating.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_Repository",
            function_name="GettblFarmerRating",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET FARMER RATING COUNT
# =====================================================
def GettblFarmerRatingCount():
    try:
        count = tblFarmerRating.select(tblFarmerRating.q.ynDeleted == False).count()
        return {"totalFarmerRatingCount": count}
    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_Repository",
            function_name="GettblFarmerRatingCount",
            payload={},
            exc=e
        )
        return {"totalFarmerRatingCount": 0}


# =====================================================
# GET FARMER RATINGS BY FARMER ID
# =====================================================
def GettblFarmerRatingByFarmerId(intFarmerId):
    try:
        row = tblFarmerRating.select(
            AND(
                tblFarmerRating.q.intFarmerId == intFarmerId,
                tblFarmerRating.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_Repository",
            function_name="GettblFarmerRatingByFarmerId",
            payload={"intFarmerId": intFarmerId},
            exc=e
        )


# =====================================================
# GET FARMER RATING BY ID
# =====================================================
def GettblFarmerRatingById(ratingId):
    try:
        return tblFarmerRating.get(ratingId)
    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_Repository",
            function_name="GettblFarmerRatingById",
            payload={"ratingId": ratingId},
            exc=e
        )
        return None


# =====================================================
# SAVE FARMER RATING
# =====================================================
def savetblFarmerRating(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblFarmerRating.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            return obj

        rating = tblFarmerRating(**JsonString)
        rating.sync()
        return rating

    except Exception as e:

        log_exception(
            file_name="tblFarmerRating_Repository",
            function_name="savetblFarmerRating",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT FARMER RATING
# =====================================================
def edittblFarmerRating(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        rating = tblFarmerRating.get(JsonString['id'])

        rating.intFarmerId = JsonString['intFarmerId']
        rating.intUserId = JsonString['intUserId']
        rating.floatRating = JsonString['floatRating']
        rating.nvcharReview = JsonString['nvcharReview']

        return rating

    except Exception as e:

        log_exception(
            file_name="tblFarmerRating_Repository",
            function_name="edittblFarmerRating",
            payload=JsonString1,
            exc=e
        )
        return None

# =====================================================
# DELETE FARMER RATING
# =====================================================
def deletetblFarmerRating(JsonString):
    try:
        rating = tblFarmerRating.get(JsonString['id'])
        rating.ynDeleted = True
        return rating

    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_Repository",
            function_name="deletetblFarmerRating",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblFarmerRating.createTable(ifNotExists=True)
