from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblOrder(SQLObject):

    intFarmerId = BigIntCol(default=None)
    intCropId = BigIntCol(default=None)
    nvcharOrderNumber = StringCol(length=100, default=None)
    intQuantity = BigIntCol(default=None)
    intUnitPrice = BigIntCol(default=None)
    intTotalPrice = BigIntCol(default=None)
    nvcharStatus = StringCol(length=50, default=None)
    intBuyerId = BigIntCol(default=None)
    nvcharDeliveryAddress = StringCol(length=500, default=None)
    
    dtOrderDate = DateTimeCol(default=datetime.now)
    dtDeliveryDate = DateTimeCol(default=None)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    
    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL ORDERS
# =====================================================
def GettblOrder():
    try:
        return list(tblOrder.select(tblOrder.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblOrder_Repository",
            function_name="GettblOrder",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET ORDER COUNT
# =====================================================
def GettblOrderCount():
    try:
        count = tblOrder.select(tblOrder.q.ynDeleted == False).count()
        return {"totalOrderCount": count}
    except Exception as e:
        log_exception(
            file_name="tblOrder_Repository",
            function_name="GettblOrderCount",
            payload={},
            exc=e
        )
        return {"totalOrderCount": 0}


# =====================================================
# GET ORDERS BY FARMER
# =====================================================
def GettblOrderByFarmerId(intFarmerId):
    try:
        row = tblOrder.select(
            AND(
                tblOrder.q.intFarmerId == intFarmerId,
                tblOrder.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblOrder_Repository",
            function_name="GettblOrderByFarmerId",
            payload={"intFarmerId": intFarmerId},
            exc=e
        )
        return []


# =====================================================
# GET ORDERS BY BUYER
# =====================================================
def GettblOrderByBuyerId(intBuyerId):
    try:
        row = tblOrder.select(
            AND(
                tblOrder.q.intBuyerId == intBuyerId,
                tblOrder.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblOrder_Repository",
            function_name="GettblOrderByBuyerId",
            payload={"intBuyerId": intBuyerId},
            exc=e
        )
        return []


# =====================================================
# SAVE ORDER
# =====================================================
def savetblOrder(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblOrder.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            order = tblOrder(**obj)
            order.sync()
            return order

    except Exception as e:
        log_exception(
            file_name="tblOrder_Repository",
            function_name="savetblOrder",
            payload=obj,
            exc=e
        )
        return None


# =====================================================
# EDIT ORDER
# =====================================================
def edittblOrder(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        order = tblOrder.get(JsonString['id'])

        order.intFarmerId = JsonString.get('intFarmerId', order.intFarmerId)
        order.intCropId = JsonString.get('intCropId', order.intCropId)
        order.nvcharOrderNumber = JsonString.get('nvcharOrderNumber', order.nvcharOrderNumber)
        order.intQuantity = JsonString.get('intQuantity', order.intQuantity)
        order.intUnitPrice = JsonString.get('intUnitPrice', order.intUnitPrice)
        order.intTotalPrice = JsonString.get('intTotalPrice', order.intTotalPrice)
        order.nvcharStatus = JsonString.get('nvcharStatus', order.nvcharStatus)
        order.intBuyerId = JsonString.get('intBuyerId', order.intBuyerId)
        order.nvcharDeliveryAddress = JsonString.get('nvcharDeliveryAddress', order.nvcharDeliveryAddress)
        order.dtDeliveryDate = JsonString.get('dtDeliveryDate', order.dtDeliveryDate)

        order.dtDateofModification = datetime.now()

        return order

    except Exception as e:
        log_exception(
            file_name="tblOrder_Repository",
            function_name="edittblOrder",
            payload=JsonString1,
            exc=e
        )
        return None


# =====================================================
# DELETE ORDER
# =====================================================
def deletetblOrder(JsonString):
    try:
        order = tblOrder.get(JsonString['id'])
        order.ynDeleted = True
        return order

    except Exception as e:
        log_exception(
            file_name="tblOrder_Repository",
            function_name="deletetblOrder",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblOrder.createTable(ifNotExists=True)
