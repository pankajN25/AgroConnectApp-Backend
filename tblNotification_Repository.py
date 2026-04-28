from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblNotification(SQLObject):

    intFarmerId = BigIntCol(default=None)
    nvcharTitle = StringCol(length=100, default=None)
    nvcharMessage = StringCol(length=500, default=None)
    nvcharNotificationType = StringCol(length=50, default=None)
    intIsRead = BoolCol(default=False)
    intPriority = BigIntCol(default=None)
    nvcharRelatedEntity = StringCol(length=100, default=None)
    intRelatedEntityId = BigIntCol(default=None)
    
    dtNotificationDate = DateTimeCol(default=datetime.now)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    
    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL NOTIFICATIONS
# =====================================================
def GettblNotification():
    try:
        return list(tblNotification.select(tblNotification.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblNotification_Repository",
            function_name="GettblNotification",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET NOTIFICATION COUNT
# =====================================================
def GettblNotificationCount():
    try:
        count = tblNotification.select(tblNotification.q.ynDeleted == False).count()
        return {"totalNotificationCount": count}
    except Exception as e:
        log_exception(
            file_name="tblNotification_Repository",
            function_name="GettblNotificationCount",
            payload={},
            exc=e
        )
        return {"totalNotificationCount": 0}


# =====================================================
# GET NOTIFICATIONS BY FARMER
# =====================================================
def GettblNotificationByFarmerId(intFarmerId):
    try:
        row = tblNotification.select(
            AND(
                tblNotification.q.intFarmerId == intFarmerId,
                tblNotification.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblNotification_Repository",
            function_name="GettblNotificationByFarmerId",
            payload={"intFarmerId": intFarmerId},
            exc=e
        )
        return []


# =====================================================
# SAVE NOTIFICATION
# =====================================================
def savetblNotification(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblNotification.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            return tblNotification(**obj)

    except Exception as e:
        log_exception(
            file_name="tblNotification_Repository",
            function_name="savetblNotification",
            payload=obj,
            exc=e
        )
        return None


# =====================================================
# EDIT NOTIFICATION
# =====================================================
def edittblNotification(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        notification = tblNotification.get(JsonString['id'])

        notification.intFarmerId = JsonString.get('intFarmerId', notification.intFarmerId)
        notification.nvcharTitle = JsonString.get('nvcharTitle', notification.nvcharTitle)
        notification.nvcharMessage = JsonString.get('nvcharMessage', notification.nvcharMessage)
        notification.nvcharNotificationType = JsonString.get('nvcharNotificationType', notification.nvcharNotificationType)
        notification.intIsRead = JsonString.get('intIsRead', notification.intIsRead)
        notification.intPriority = JsonString.get('intPriority', notification.intPriority)
        notification.nvcharRelatedEntity = JsonString.get('nvcharRelatedEntity', notification.nvcharRelatedEntity)
        notification.intRelatedEntityId = JsonString.get('intRelatedEntityId', notification.intRelatedEntityId)

        notification.dtDateofModification = datetime.now()

        return notification

    except Exception as e:
        log_exception(
            file_name="tblNotification_Repository",
            function_name="edittblNotification",
            payload=JsonString1,
            exc=e
        )
        return None


# =====================================================
# DELETE NOTIFICATION
# =====================================================
def deletetblNotification(JsonString):
    try:
        notification = tblNotification.get(JsonString['id'])
        notification.ynDeleted = True
        return notification

    except Exception as e:
        log_exception(
            file_name="tblNotification_Repository",
            function_name="deletetblNotification",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblNotification.createTable(ifNotExists=True)
