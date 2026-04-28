from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblChatMessage(SQLObject):

    intChatRoomId = BigIntCol(default=None)
    intSenderId = BigIntCol(default=None)
    nvcharMessage = StringCol(length=1000, default=None)
    nvcharMessageType = StringCol(length=50, default=None)
    intIsRead = BoolCol(default=False)
    
    dtMessageDate = DateTimeCol(default=datetime.now)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    
    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL CHAT MESSAGES
# =====================================================
def GettblChatMessage():
    try:
        return list(tblChatMessage.select(tblChatMessage.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblChatMessage_Repository",
            function_name="GettblChatMessage",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET CHAT MESSAGE COUNT
# =====================================================
def GettblChatMessageCount():
    try:
        count = tblChatMessage.select(tblChatMessage.q.ynDeleted == False).count()
        return {"totalChatMessageCount": count}
    except Exception as e:
        log_exception(
            file_name="tblChatMessage_Repository",
            function_name="GettblChatMessageCount",
            payload={},
            exc=e
        )
        return {"totalChatMessageCount": 0}


# =====================================================
# GET MESSAGES BY ROOM
# =====================================================
def GettblChatMessageByChatRoomId(intChatRoomId):
    try:
        row = tblChatMessage.select(
            AND(
                tblChatMessage.q.intChatRoomId == intChatRoomId,
                tblChatMessage.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblChatMessage_Repository",
            function_name="GettblChatMessageByChatRoomId",
            payload={"intChatRoomId": intChatRoomId},
            exc=e
        )
        return []


# =====================================================
# SAVE CHAT MESSAGE
# =====================================================
def savetblChatMessage(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblChatMessage.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            return tblChatMessage(**obj)

    except Exception as e:
        log_exception(
            file_name="tblChatMessage_Repository",
            function_name="savetblChatMessage",
            payload=obj,
            exc=e
        )
        return None


# =====================================================
# EDIT CHAT MESSAGE
# =====================================================
def edittblChatMessage(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        message = tblChatMessage.get(JsonString['id'])

        message.nvcharMessage = JsonString.get('nvcharMessage', message.nvcharMessage)
        message.intIsRead = JsonString.get('intIsRead', message.intIsRead)

        message.dtDateofModification = datetime.now()

        return message

    except Exception as e:
        log_exception(
            file_name="tblChatMessage_Repository",
            function_name="edittblChatMessage",
            payload=JsonString1,
            exc=e
        )
        return None


# =====================================================
# DELETE CHAT MESSAGE
# =====================================================
def deletetblChatMessage(JsonString):
    try:
        message = tblChatMessage.get(JsonString['id'])
        message.ynDeleted = True
        return message

    except Exception as e:
        log_exception(
            file_name="tblChatMessage_Repository",
            function_name="deletetblChatMessage",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblChatMessage.createTable(ifNotExists=True)
