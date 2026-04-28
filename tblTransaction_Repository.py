from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblTransaction(SQLObject):

    intOrderId = BigIntCol(default=None)
    nvcharTransactionNo = StringCol(length=100)
    floatAmount = FloatCol(default=0)
    nvcharPaymentMethod = StringCol(length=100)
    nvcharPaymentStatus = StringCol(length=50)
    dtTransactionDate = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL TRANSACTIONS
# =====================================================
def GettblTransaction():
    try:
        return list(tblTransaction.select(tblTransaction.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblTransaction_Repository",
            function_name="GettblTransaction",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET TRANSACTION COUNT
# =====================================================
def GettblTransactionCount():
    try:
        count = tblTransaction.select(tblTransaction.q.ynDeleted == False).count()
        return {"totalTransactionCount": count}
    except Exception as e:
        log_exception(
            file_name="tblTransaction_Repository",
            function_name="GettblTransactionCount",
            payload={},
            exc=e
        )
        return {"totalTransactionCount": 0}


# =====================================================
# GET TRANSACTIONS BY ORDER ID
# =====================================================
def GettblTransactionByOrderId(intOrderId):
    try:
        row = tblTransaction.select(
            AND(
                tblTransaction.q.intOrderId == intOrderId,
                tblTransaction.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblTransaction_Repository",
            function_name="GettblTransactionByOrderId",
            payload={"intOrderId": intOrderId},
            exc=e
        )


# =====================================================
# GET TRANSACTION BY ID
# =====================================================
def GettblTransactionById(transactionId):
    try:
        return tblTransaction.get(transactionId)
    except Exception as e:
        log_exception(
            file_name="tblTransaction_Repository",
            function_name="GettblTransactionById",
            payload={"transactionId": transactionId},
            exc=e
        )
        return None


# =====================================================
# SAVE TRANSACTION
# =====================================================
def savetblTransaction(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblTransaction.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            return obj

        return tblTransaction(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblTransaction_Repository",
            function_name="savetblTransaction",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT TRANSACTION
# =====================================================
def edittblTransaction(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        transaction = tblTransaction.get(JsonString['id'])

        transaction.intOrderId = JsonString['intOrderId']
        transaction.nvcharTransactionNo = JsonString['nvcharTransactionNo']
        transaction.floatAmount = JsonString['floatAmount']
        transaction.nvcharPaymentMethod = JsonString['nvcharPaymentMethod']
        transaction.nvcharPaymentStatus = JsonString['nvcharPaymentStatus']

        return transaction

    except Exception as e:

        log_exception(
            file_name="tblTransaction_Repository",
            function_name="edittblTransaction",
            payload=JsonString1,
            exc=e
        )
        return None

# =====================================================
# DELETE TRANSACTION
# =====================================================
def deletetblTransaction(JsonString):
    try:
        transaction = tblTransaction.get(JsonString['id'])
        transaction.ynDeleted = True
        return transaction

    except Exception as e:
        log_exception(
            file_name="tblTransaction_Repository",
            function_name="deletetblTransaction",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblTransaction.createTable(ifNotExists=True)
