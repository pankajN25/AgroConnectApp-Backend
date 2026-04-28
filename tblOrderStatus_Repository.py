from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblOrderStatus(SQLObject):

    intOrderId = BigIntCol(default=None)
    nvcharStatus = StringCol(length=100)
    nvcharDescription = StringCol(length=300)
    dtStatusDatetime = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL ORDER STATUS
# =====================================================
def GettblOrderStatus():
    try:
        return list(tblOrderStatus.select(tblOrderStatus.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_Repository",
            function_name="GettblOrderStatus",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET ORDER STATUS COUNT
# =====================================================
def GettblOrderStatusCount():
    try:
        count = tblOrderStatus.select(tblOrderStatus.q.ynDeleted == False).count()
        return {"totalOrderStatusCount": count}
    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_Repository",
            function_name="GettblOrderStatusCount",
            payload={},
            exc=e
        )
        return {"totalOrderStatusCount": 0}


# =====================================================
# GET ORDER STATUS BY ORDER ID
# =====================================================
def GettblOrderStatusByOrderId(intOrderId):
    try:
        row = tblOrderStatus.select(
            AND(
                tblOrderStatus.q.intOrderId == intOrderId,
                tblOrderStatus.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_Repository",
            function_name="GettblOrderStatusByOrderId",
            payload={"intOrderId": intOrderId},
            exc=e
        )


# =====================================================
# GET ORDER STATUS BY ID
# =====================================================
def GettblOrderStatusById(statusId):
    try:
        return tblOrderStatus.get(statusId)
    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_Repository",
            function_name="GettblOrderStatusById",
            payload={"statusId": statusId},
            exc=e
        )
        return None


# =====================================================
# SAVE ORDER STATUS
# =====================================================
def savetblOrderStatus(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblOrderStatus.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            return obj

        return tblOrderStatus(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblOrderStatus_Repository",
            function_name="savetblOrderStatus",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT ORDER STATUS
# =====================================================
def edittblOrderStatus(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        status = tblOrderStatus.get(JsonString['id'])

        status.intOrderId = JsonString['intOrderId']
        status.nvcharStatus = JsonString['nvcharStatus']
        status.nvcharDescription = JsonString['nvcharDescription']

        return status

    except Exception as e:

        log_exception(
            file_name="tblOrderStatus_Repository",
            function_name="edittblOrderStatus",
            payload=JsonString1,
            exc=e
        )
        return None

# =====================================================
# DELETE ORDER STATUS
# =====================================================
def deletetblOrderStatus(JsonString):
    try:
        status = tblOrderStatus.get(JsonString['id'])
        status.ynDeleted = True
        return status

    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_Repository",
            function_name="deletetblOrderStatus",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblOrderStatus.createTable(ifNotExists=True)
