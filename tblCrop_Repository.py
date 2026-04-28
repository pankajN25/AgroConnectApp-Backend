from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
import sqlite3
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblCrop(SQLObject):

    intFarmerId = BigIntCol(default=None)
    nvcharCropName = StringCol(length=150, default=None)
    intCropCategoryId = BigIntCol(default=None)
    floatQuantity = FloatCol(default=0)
    floatPricePerKg = FloatCol(default=0)
    dtHarvestDate = DateCol(default=None)
    nvcharDescription = StringCol(length=500, default=None)
    nvcharLocation = StringCol(length=200, default=None)
    # Keep DB column names aligned with existing camelCase columns in sqlite
    floatLatitude = FloatCol(default=None, dbName="floatLatitude")
    floatLongitude = FloatCol(default=None, dbName="floatLongitude")
    intQualityGradeId = BigIntCol(default=None)
    ynOrganic = BoolCol(default=False)
    nvcharCropImageUrl = StringCol(length=300, default=None)
    nvcharStatus = StringCol(length=50, default="ACTIVE")
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL CROPS
# =====================================================
def GettblCrop():
    try:
        return list(tblCrop.select(tblCrop.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblCrop_Repository",
            function_name="GettblCrop",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET CROP COUNT
# =====================================================
def GettblCropCount():
    try:
        count = tblCrop.select(tblCrop.q.ynDeleted == False).count()
        return {"totalCropCount": count}
    except Exception as e:
        log_exception(
            file_name="tblCrop_Repository",
            function_name="GettblCropCount",
            payload={},
            exc=e
        )
        return {"totalCropCount": 0}


# =====================================================
# GET CROPS BY FARMER ID
# =====================================================
def GettblCropByFarmerId(intFarmerId):
    try:
        rows = list(tblCrop.select(
            AND(
                tblCrop.q.intFarmerId == intFarmerId,
                tblCrop.q.ynDeleted == False
            )
        ))
        result = []
        for r in rows:
            result.append({
                "id": r.id,
                "intFarmerId": r.intFarmerId,
                "nvcharCropName": r.nvcharCropName,
                "intCropCategoryId": r.intCropCategoryId,
                "floatQuantity": r.floatQuantity,
                "floatPricePerKg": r.floatPricePerKg,
                "dtHarvestDate": str(r.dtHarvestDate) if r.dtHarvestDate else None,
                "nvcharDescription": r.nvcharDescription,
                "nvcharLocation": r.nvcharLocation,
                "floatLatitude": r.floatLatitude,
                "floatLongitude": r.floatLongitude,
                "intQualityGradeId": r.intQualityGradeId,
                "ynOrganic": r.ynOrganic,
                "nvcharCropImageUrl": r.nvcharCropImageUrl,
                "nvcharStatus": r.nvcharStatus,
                "dtDateOfCreation": str(r.dtDateOfCreation) if r.dtDateOfCreation else None,
            })
        return result
    except Exception as e:
        log_exception(
            file_name="tblCrop_Repository",
            function_name="GettblCropByFarmerId",
            payload={"intFarmerId": intFarmerId},
            exc=e
        )
        return []


# =====================================================
# GET CROPS BY CATEGORY
# =====================================================
def GettblCropByCategoryId(intCropCategoryId):
    try:
        row = tblCrop.select(
            AND(
                tblCrop.q.intCropCategoryId == intCropCategoryId,
                tblCrop.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblCrop_Repository",
            function_name="GettblCropByCategoryId",
            payload={"intCropCategoryId": intCropCategoryId},
            exc=e
        )
        return []


# =====================================================
# SAVE CROP
# =====================================================
def savetblCrop(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblCrop.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            obj.dtDateofModification = datetime.now()

            return obj

        return tblCrop(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblCrop_Repository",
            function_name="savetblCrop",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT CROP
# =====================================================
def edittblCrop(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        crop = tblCrop.get(JsonString['id'])

        crop.nvcharCropName = JsonString['nvcharCropName']
        crop.intCropCategoryId = JsonString['intCropCategoryId']
        crop.floatQuantity = JsonString['floatQuantity']
        crop.floatPricePerKg = JsonString['floatPricePerKg']
        crop.dtHarvestDate = JsonString['dtHarvestDate']
        crop.nvcharDescription = JsonString['nvcharDescription']
        crop.nvcharLocation = JsonString['nvcharLocation']
        if 'floatLatitude' in JsonString:
            crop.floatLatitude = JsonString.get('floatLatitude')
        if 'floatLongitude' in JsonString:
            crop.floatLongitude = JsonString.get('floatLongitude')
        crop.intQualityGradeId = JsonString['intQualityGradeId']
        crop.ynOrganic = JsonString['ynOrganic']
        crop.nvcharCropImageUrl = JsonString['nvcharCropImageUrl']

        crop.dtDateofModification = datetime.now()

        return crop

    except Exception as e:

        log_exception(
            file_name="tblCrop_Repository",
            function_name="edittblCrop",
            payload=JsonString1,
            exc=e
        )
        

# =====================================================
# DELETE CROP
# =====================================================
def deletetblCrop(JsonString):
    try:
        crop = tblCrop.get(JsonString['id'])
        crop.ynDeleted = True
        return crop

    except Exception as e:
        log_exception(
            file_name="tblCrop_Repository",
            function_name="deletetblCrop",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblCrop.createTable(ifNotExists=True)

# =====================================================
# LIGHTWEIGHT MIGRATION (ADD LAT/LONG IF MISSING)
# =====================================================
def ensure_lat_long_columns():
    try:
        conn = sqlite3.connect("world.sqlite3")
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(tbl_crop)")
        cols = [row[1] for row in cur.fetchall()]
        has_camel_lat = "floatLatitude" in cols
        has_camel_lng = "floatLongitude" in cols
        has_snake_lat = "float_latitude" in cols
        has_snake_lng = "float_longitude" in cols

        # Prefer camelCase columns (matches current DB + model mapping)
        if not has_camel_lat:
            cur.execute("ALTER TABLE tbl_crop ADD COLUMN floatLatitude REAL")
            if has_snake_lat:
                cur.execute("UPDATE tbl_crop SET floatLatitude = float_latitude")
        if not has_camel_lng:
            cur.execute("ALTER TABLE tbl_crop ADD COLUMN floatLongitude REAL")
            if has_snake_lng:
                cur.execute("UPDATE tbl_crop SET floatLongitude = float_longitude")

        # If only camelCase exists, do not add snake_case columns.
        conn.commit()
        conn.close()
    except Exception as e:
        log_exception(
            file_name="tblCrop_Repository",
            function_name="ensure_lat_long_columns",
            payload={},
            exc=e
        )

ensure_lat_long_columns()
