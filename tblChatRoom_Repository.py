from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblChatRoom(SQLObject):

    nvcharRoomName = StringCol(length=100, default=None)
    intCreatedBy = BigIntCol(default=None)
    intParticipantCount = BigIntCol(default=0)
    nvcharRoomType = StringCol(length=50, default=None)
    nvcharDescription = StringCol(length=500, default=None)
    
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    
    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL CHAT ROOMS
# =====================================================
def GettblChatRoom():
    try:
        return list(tblChatRoom.select(tblChatRoom.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblChatRoom_Repository",
            function_name="GettblChatRoom",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET CHAT ROOM COUNT
# =====================================================
def GettblChatRoomCount():
    try:
        count = tblChatRoom.select(tblChatRoom.q.ynDeleted == False).count()
        return {"totalChatRoomCount": count}
    except Exception as e:
        log_exception(
            file_name="tblChatRoom_Repository",
            function_name="GettblChatRoomCount",
            payload={},
            exc=e
        )
        return {"totalChatRoomCount": 0}


# =====================================================
# GET CHAT ROOMS BY USER
# =====================================================
def GettblChatRoomByCreatedBy(intCreatedBy):
    try:
        row = tblChatRoom.select(
            AND(
                tblChatRoom.q.intCreatedBy == intCreatedBy,
                tblChatRoom.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblChatRoom_Repository",
            function_name="GettblChatRoomByCreatedBy",
            payload={"intCreatedBy": intCreatedBy},
            exc=e
        )
        return []


# =====================================================
# SAVE CHAT ROOM
# =====================================================
def savetblChatRoom(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblChatRoom.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            return tblChatRoom(**obj)

    except Exception as e:
        log_exception(
            file_name="tblChatRoom_Repository",
            function_name="savetblChatRoom",
            payload=obj,
            exc=e
        )
        return None


# =====================================================
# EDIT CHAT ROOM
# =====================================================
def edittblChatRoom(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        room = tblChatRoom.get(JsonString['id'])

        room.nvcharRoomName = JsonString.get('nvcharRoomName', room.nvcharRoomName)
        room.intParticipantCount = JsonString.get('intParticipantCount', room.intParticipantCount)
        room.nvcharRoomType = JsonString.get('nvcharRoomType', room.nvcharRoomType)
        room.nvcharDescription = JsonString.get('nvcharDescription', room.nvcharDescription)

        room.dtDateofModification = datetime.now()

        return room

    except Exception as e:
        log_exception(
            file_name="tblChatRoom_Repository",
            function_name="edittblChatRoom",
            payload=JsonString1,
            exc=e
        )
        return None


# =====================================================
# DELETE CHAT ROOM
# =====================================================
def deletetblChatRoom(JsonString):
    try:
        room = tblChatRoom.get(JsonString['id'])
        room.ynDeleted = True
        return room

    except Exception as e:
        log_exception(
            file_name="tblChatRoom_Repository",
            function_name="deletetblChatRoom",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblChatRoom.createTable(ifNotExists=True)
