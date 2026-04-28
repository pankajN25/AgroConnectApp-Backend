
import sys
from sqlobject import SQLObject
from datetime import datetime
from sqlobject import *
# from db_connection import init_db
# from db_connection import init_db_pool as init_db
from CommonFunction import *
from fastapi.responses import JSONResponse

# ✅ Initialize MySQL DB connection (MANDATORY before defining model)
# connection = init_db()
# from db_connection import get_connection

# connection = get_connection()

class tblLanguage(SQLObject):
    # _connection = connection
    languagename = StringCol(length=500, default=None)
    nvcharDescription = StringCol(length=500, default=None)
    dtDateOfCreation = DateTimeCol(default=datetime.datetime.now())
    dtDateofModification = DateTimeCol(default=None)
    ynDeleted = BoolCol(default=False)


def GettableLanguage():
    try:
        Res = tblLanguage.select(AND(tblLanguage.q.ynDeleted == False))
        return Res
    except Exception as e:
        log_exception(
            file_name="tblLanguageRepository",
            function_name="GettableLanguage",
            payload=None,
            exc=e
        )
        return None

def GettblLanguageById(Jid):
    try:
        row = tblLanguage.get(Jid)
        if Jid is None:
            return JSONResponse({"error": "Missing or invalid JSON in request body"}), 400
        return row
    except Exception as e:
        log_exception(
            file_name="tblLanguageRepository",
            function_name="GettblLanguageById",
            payload={"id": Jid},
            exc=e
        )
        return None


def savetblLanguage(JsonString):
    try:
        jstr = json.dumps(JsonString)
        obj = json.loads(jstr, object_hook=datetime_decoder)
        oRepository = tblLanguage(**obj)
        return oRepository
    except Exception as e:
        log_exception(
            file_name="tblLanguageRepository",
            function_name="savetblLanguage",
            payload=JsonString,
            exc=e
        )
        return None




def edittblLanguage(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)
        tblLanguageRepository = tblLanguage.get(JsonString['id'])
        tblLanguageRepository.languagename = JsonString['languagename']
        tblLanguageRepository.nvcharDescription = JsonString['nvcharDescription']
        tblLanguageRepository.updated_at = datetime.datetime.now()
        return tblLanguageRepository
    except Exception as e:
        log_exception(
            file_name="tblLanguageRepository",
            function_name="edittblLanguage",
            payload=JsonString1,
            exc=e
        )
        return None


def deletetblLanguage(JsonString):
    try:
        oRepository = tblLanguage.get(JsonString['id'])
        oRepository.ynDeleted = True
        return oRepository
    except Exception as e:
        log_exception(
            file_name="tblLanguageRepository",
            function_name="deletetblLanguage",
            payload=JsonString,
            exc=e
        )
        return None


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblLanguage.createTable(ifNotExists=True)


# # ✅ Create table directly in MySQL
# tblLanguage.createTable(ifNotExists=True)