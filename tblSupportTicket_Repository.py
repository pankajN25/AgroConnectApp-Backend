from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblSupportTicket(SQLObject):

    intUserId = BigIntCol(default=None)
    nvcharSubject = StringCol(length=200)
    nvcharMessage = StringCol(length=500)
    nvcharStatus = StringCol(length=50)
    dtCreatedDatetime = DateTimeCol(default=datetime.now)
    ynDeleted = BoolCol(default=False)

# =====================================================
# GET ALL SUPPORT TICKETS
# =====================================================
def GettblSupportTicket():
    try:
        return list(tblSupportTicket.select(tblSupportTicket.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_Repository",
            function_name="GettblSupportTicket",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET SUPPORT TICKET COUNT
# =====================================================
def GettblSupportTicketCount():
    try:
        count = tblSupportTicket.select(tblSupportTicket.q.ynDeleted == False).count()
        return {"totalSupportTicketCount": count}
    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_Repository",
            function_name="GettblSupportTicketCount",
            payload={},
            exc=e
        )
        return {"totalSupportTicketCount": 0}


# =====================================================
# GET SUPPORT TICKETS BY USER ID
# =====================================================
def GettblSupportTicketByUserId(intUserId):
    try:
        row = tblSupportTicket.select(
            AND(
                tblSupportTicket.q.intUserId == intUserId,
                tblSupportTicket.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_Repository",
            function_name="GettblSupportTicketByUserId",
            payload={"intUserId": intUserId},
            exc=e
        )


# =====================================================
# GET SUPPORT TICKET BY ID
# =====================================================
def GettblSupportTicketById(ticketId):
    try:
        return tblSupportTicket.get(ticketId)
    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_Repository",
            function_name="GettblSupportTicketById",
            payload={"ticketId": ticketId},
            exc=e
        )
        return None


# =====================================================
# SAVE SUPPORT TICKET
# =====================================================
def savetblSupportTicket(JsonString):

    try:

        if JsonString.get("id"):

            obj = tblSupportTicket.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            return obj

        return tblSupportTicket(**JsonString)

    except Exception as e:

        log_exception(
            file_name="tblSupportTicket_Repository",
            function_name="savetblSupportTicket",
            payload=JsonString,
            exc=e
        )

        return None


# =====================================================
# EDIT SUPPORT TICKET
# =====================================================
def edittblSupportTicket(JsonString1):

    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        ticket = tblSupportTicket.get(JsonString['id'])

        ticket.intUserId = JsonString['intUserId']
        ticket.nvcharSubject = JsonString['nvcharSubject']
        ticket.nvcharMessage = JsonString['nvcharMessage']
        ticket.nvcharStatus = JsonString['nvcharStatus']

        return ticket

    except Exception as e:

        log_exception(
            file_name="tblSupportTicket_Repository",
            function_name="edittblSupportTicket",
            payload=JsonString1,
            exc=e
        )
        return None

# =====================================================
# DELETE SUPPORT TICKET
# =====================================================
def deletetblSupportTicket(JsonString):
    try:
        ticket = tblSupportTicket.get(JsonString['id'])
        ticket.ynDeleted = True
        return ticket

    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_Repository",
            function_name="deletetblSupportTicket",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblSupportTicket.createTable(ifNotExists=True)
