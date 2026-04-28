from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblCropHealthScan(SQLObject):

    intCropId = BigIntCol(default=None)
    intFarmerId = BigIntCol(default=None)
    nvcharDiseaseDetected = StringCol(length=100, default=None)
    intSeverity = BigIntCol(default=None)
    nvcharTreatmentRecommendation = StringCol(length=500, default=None)
    nvcharImagePath = StringCol(length=500, default=None)
    intHealthScore = BigIntCol(default=None)
    
    dtScanDate = DateTimeCol(default=datetime.now)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    
    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL CROP HEALTH SCANS
# =====================================================
def GettblCropHealthScan():
    try:
        return list(tblCropHealthScan.select(tblCropHealthScan.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblCropHealthScan_Repository",
            function_name="GettblCropHealthScan",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET CROP HEALTH SCAN COUNT
# =====================================================
def GettblCropHealthScanCount():
    try:
        count = tblCropHealthScan.select(tblCropHealthScan.q.ynDeleted == False).count()
        return {"totalCropHealthScanCount": count}
    except Exception as e:
        log_exception(
            file_name="tblCropHealthScan_Repository",
            function_name="GettblCropHealthScanCount",
            payload={},
            exc=e
        )
        return {"totalCropHealthScanCount": 0}


# =====================================================
# GET SCANS BY FARMER
# =====================================================
def GettblCropHealthScanByFarmerId(intFarmerId):
    try:
        row = tblCropHealthScan.select(
            AND(
                tblCropHealthScan.q.intFarmerId == intFarmerId,
                tblCropHealthScan.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblCropHealthScan_Repository",
            function_name="GettblCropHealthScanByFarmerId",
            payload={"intFarmerId": intFarmerId},
            exc=e
        )
        return []


# =====================================================
# SAVE CROP HEALTH SCAN
# =====================================================
def savetblCropHealthScan(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblCropHealthScan.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            return tblCropHealthScan(**obj)

    except Exception as e:
        log_exception(
            file_name="tblCropHealthScan_Repository",
            function_name="savetblCropHealthScan",
            payload=obj,
            exc=e
        )
        return None


# =====================================================
# EDIT CROP HEALTH SCAN
# =====================================================
def edittblCropHealthScan(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        scan = tblCropHealthScan.get(JsonString['id'])

        scan.intCropId = JsonString.get('intCropId', scan.intCropId)
        scan.intFarmerId = JsonString.get('intFarmerId', scan.intFarmerId)
        scan.nvcharDiseaseDetected = JsonString.get('nvcharDiseaseDetected', scan.nvcharDiseaseDetected)
        scan.intSeverity = JsonString.get('intSeverity', scan.intSeverity)
        scan.nvcharTreatmentRecommendation = JsonString.get('nvcharTreatmentRecommendation', scan.nvcharTreatmentRecommendation)
        scan.nvcharImagePath = JsonString.get('nvcharImagePath', scan.nvcharImagePath)
        scan.intHealthScore = JsonString.get('intHealthScore', scan.intHealthScore)

        scan.dtDateofModification = datetime.now()

        return scan

    except Exception as e:
        log_exception(
            file_name="tblCropHealthScan_Repository",
            function_name="edittblCropHealthScan",
            payload=JsonString1,
            exc=e
        )
        return None


# =====================================================
# DELETE CROP HEALTH SCAN
# =====================================================
def deletetblCropHealthScan(JsonString):
    try:
        scan = tblCropHealthScan.get(JsonString['id'])
        scan.ynDeleted = True
        return scan

    except Exception as e:
        log_exception(
            file_name="tblCropHealthScan_Repository",
            function_name="deletetblCropHealthScan",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblCropHealthScan.createTable(ifNotExists=True)
