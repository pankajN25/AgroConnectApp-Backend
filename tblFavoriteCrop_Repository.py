from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblFavoriteCrop(SQLObject):

    intUserId = BigIntCol(default=None)
    intCropId = BigIntCol(default=None)
    dtCreatedDatetime = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL FAVORITE CROPS
# =====================================================
def GettblFavoriteCrop():
    try:
        return list(tblFavoriteCrop.select(tblFavoriteCrop.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_Repository",
            function_name="GettblFavoriteCrop",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET FAVORITE CROP COUNT
# =====================================================
def GettblFavoriteCropCount():
    try:
        count = tblFavoriteCrop.select(tblFavoriteCrop.q.ynDeleted == False).count()
        return {"totalFavoriteCropsCount": count}
    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_Repository",
            function_name="GettblFavoriteCropCount",
            payload={},
            exc=e
        )
        return {"totalFavoriteCropsCount": 0}


# =====================================================
# GET FAVORITE CROPS BY USER ID
# =====================================================
def GettblFavoriteCropByUserId(intUserId):
    try:
        row = tblFavoriteCrop.select(
            AND(
                tblFavoriteCrop.q.intUserId == intUserId,
                tblFavoriteCrop.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_Repository",
            function_name="GettblFavoriteCropByUserId",
            payload={"intUserId": intUserId},
            exc=e
        )


# =====================================================
# GET FAVORITE CROP BY ID
# =====================================================
def GettblFavoriteCropById(favoriteId):
    try:
        return tblFavoriteCrop.get(favoriteId)
    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_Repository",
            function_name="GettblFavoriteCropById",
            payload={"favoriteId": favoriteId},
            exc=e
        )
        return None


# =====================================================
# SAVE FAVORITE CROP
# =====================================================
def savetblFavoriteCrop(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblFavoriteCrop.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            return obj

        return tblFavoriteCrop(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblFavoriteCrop_Repository",
            function_name="savetblFavoriteCrop",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT FAVORITE CROP
# =====================================================
def edittblFavoriteCrop(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        favorite = tblFavoriteCrop.get(JsonString['id'])

        favorite.intUserId = JsonString['intUserId']
        favorite.intCropId = JsonString['intCropId']

        return favorite

    except Exception as e:

        log_exception(
            file_name="tblFavoriteCrop_Repository",
            function_name="edittblFavoriteCrop",
            payload=JsonString1,
            exc=e
        )
        return None

# =====================================================
# DELETE FAVORITE CROP
# =====================================================
def deletetblFavoriteCrop(JsonString):
    try:
        favorite = tblFavoriteCrop.get(JsonString['id'])
        favorite.ynDeleted = True
        return favorite

    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_Repository",
            function_name="deletetblFavoriteCrop",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblFavoriteCrop.createTable(ifNotExists=True)
