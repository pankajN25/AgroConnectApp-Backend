from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblDirectMessage(SQLObject):

    intSenderId = BigIntCol(default=None)
    intReceiverId = BigIntCol(default=None)
    nvcharMessage = StringCol(length=1000, default=None)

    dtMessageDate = DateTimeCol(default=datetime.now)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)

    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL MESSAGES
# =====================================================
def GettblDirectMessage():
    try:
        return list(tblDirectMessage.select(tblDirectMessage.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblDirectMessage_Repository",
            function_name="GettblDirectMessage",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET MESSAGES BETWEEN USERS
# =====================================================
def GettblDirectMessageByUsers(intUserId1, intUserId2):
    try:
        row = tblDirectMessage.select(
            AND(
                OR(
                    AND(
                        tblDirectMessage.q.intSenderId == intUserId1,
                        tblDirectMessage.q.intReceiverId == intUserId2
                    ),
                    AND(
                        tblDirectMessage.q.intSenderId == intUserId2,
                        tblDirectMessage.q.intReceiverId == intUserId1
                    )
                ),
                tblDirectMessage.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblDirectMessage_Repository",
            function_name="GettblDirectMessageByUsers",
            payload={"intUserId1": intUserId1, "intUserId2": intUserId2},
            exc=e
        )
        return []


# =====================================================
# GET MESSAGES BY USER
# =====================================================
def GettblDirectMessageByUser(intUserId):
    try:
        row = tblDirectMessage.select(
            AND(
                OR(
                    tblDirectMessage.q.intSenderId == intUserId,
                    tblDirectMessage.q.intReceiverId == intUserId
                ),
                tblDirectMessage.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblDirectMessage_Repository",
            function_name="GettblDirectMessageByUser",
            payload={"intUserId": intUserId},
            exc=e
        )
        return []

# =====================================================
# SAVE MESSAGE
# =====================================================
def savetblDirectMessage(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblDirectMessage.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            msg = tblDirectMessage(**obj)
            msg.sync()
            return msg

    except Exception as e:
        log_exception(
            file_name="tblDirectMessage_Repository",
            function_name="savetblDirectMessage",
            payload=obj,
            exc=e
        )
        return None


# =====================================================
# EDIT MESSAGE
# =====================================================
def edittblDirectMessage(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        message = tblDirectMessage.get(JsonString['id'])
        message.nvcharMessage = JsonString.get('nvcharMessage', message.nvcharMessage)
        message.dtDateofModification = datetime.now()
        return message

    except Exception as e:
        log_exception(
            file_name="tblDirectMessage_Repository",
            function_name="edittblDirectMessage",
            payload=JsonString1,
            exc=e
        )
        return None


# =====================================================
# DELETE MESSAGE
# =====================================================
def deletetblDirectMessage(JsonString):
    try:
        message = tblDirectMessage.get(JsonString['id'])
        message.ynDeleted = True
        return message

    except Exception as e:
        log_exception(
            file_name="tblDirectMessage_Repository",
            function_name="deletetblDirectMessage",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblDirectMessage.createTable(ifNotExists=True)
