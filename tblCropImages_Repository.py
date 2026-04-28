from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblCropImages(SQLObject):

    intCropId = BigIntCol(default=None)
    nvcharImageUrl = StringCol(length=500, default=None)
    ynPrimary = BoolCol(default=False)
    dtCreatedDatetime = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL CROP IMAGES
# =====================================================
def GettblCropImages():
    try:
        return list(tblCropImages.select(tblCropImages.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblCropImages_Repository",
            function_name="GettblCropImages",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET CROP IMAGE COUNT
# =====================================================
def GettblCropImagesCount():
    try:
        count = tblCropImages.select(tblCropImages.q.ynDeleted == False).count()
        return {"totalCropImagesCount": count}
    except Exception as e:
        log_exception(
            file_name="tblCropImages_Repository",
            function_name="GettblCropImagesCount",
            payload={},
            exc=e
        )
        return {"totalCropImagesCount": 0}


# =====================================================
# GET CROP IMAGES BY CROP ID
# =====================================================
def GettblCropImagesByCropId(intCropId):
    try:
        row = tblCropImages.select(
            AND(
                tblCropImages.q.intCropId == intCropId,
                tblCropImages.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblCropImages_Repository",
            function_name="GettblCropImagesByCropId",
            payload={"intCropId": intCropId},
            exc=e
        )


# =====================================================
# GET CROP IMAGE BY ID
# =====================================================
def GettblCropImagesById(imageId):
    try:
        return tblCropImages.get(imageId)
    except Exception as e:
        log_exception(
            file_name="tblCropImages_Repository",
            function_name="GettblCropImagesById",
            payload={"imageId": imageId},
            exc=e
        )
        return None


# =====================================================
# SAVE CROP IMAGE
# =====================================================
def savetblCropImages(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblCropImages.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            return obj

        return tblCropImages(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblCropImages_Repository",
            function_name="savetblCropImages",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT CROP IMAGE
# =====================================================
def edittblCropImages(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        image = tblCropImages.get(JsonString['id'])

        image.intCropId = JsonString['intCropId']
        image.nvcharImageUrl = JsonString['nvcharImageUrl']
        image.ynPrimary = JsonString['ynPrimary']

        return image

    except Exception as e:

        log_exception(
            file_name="tblCropImages_Repository",
            function_name="edittblCropImages",
            payload=JsonString1,
            exc=e
        )

# =====================================================
# DELETE CROP IMAGE
# =====================================================
def deletetblCropImages(JsonString):
    try:
        image = tblCropImages.get(JsonString['id'])
        image.ynDeleted = True
        return image

    except Exception as e:
        log_exception(
            file_name="tblCropImages_Repository",
            function_name="deletetblCropImages",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblCropImages.createTable(ifNotExists=True)
