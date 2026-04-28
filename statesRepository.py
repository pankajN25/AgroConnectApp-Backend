import sys

from datetime import datetime
from sqlobject import *

# from db_connection import init_db_pool as init_db
from CommonFunction import *
from fastapi.responses import JSONResponse

# ✅ Initialize MySQL DB connection (MANDATORY before defining model)
# connection = init_db()
# from db_connection import get_connection

# connection = get_connection()

class States(SQLObject):
    # _connection = connection
    name = StringCol(length=100, default=None)
    country_id = BigIntCol(default=None)
    country_code = StringCol(length=50, default=None)
    fips_code = StringCol(length=255, default=None)
    iso2 = StringCol(length=255, default=None)
    type = StringCol(length=255, default=None)
    level = BigIntCol(default=None)
    parent_id = BigIntCol(default=None)
    latitude = FloatCol(default=None)
    longitude = FloatCol(default=None)
    created_at = DateTimeCol(default=datetime.datetime.now())
    updated_at = DateTimeCol(default=None)
    flag = BigIntCol(default=None)
    wikiDataId = StringCol(length=50, default=None)


def GetStates():
    try:
        Res = States.select()
        return Res
    except:
        print("error in States.GetStates", sys.exc_info()[1])


# def GetStatesById(Jid):
#     try:
#         row = States.get(Jid)
#         if Jid is None:
#             return jsonify({"error": "Missing or invalid JSON in request body"}), 400
#         return row
#     except:
#         print("error in States.GetStatesById", sys.exc_info()[1])

def GetStatesById(Jid):
    try:
        return States.get(Jid)
    except Exception as e:
        print("error in States.GetStatesById error:", e)


def GetStatesByCountry_id(country_id):
    try:
        row = States.select(AND(States.q.country_id == country_id))
        return row
    except:
        print("error in States.GetStatesByCountry_id", sys.exc_info()[1])


def GetStatesByCountry_code(country_code):
    try:
        row = States.select(AND(States.q.country_code == country_code))
        return row
    except:
        print("error in States.GetStatesByCountry_code", sys.exc_info()[1])


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
States.createTable(ifNotExists=True)


# # ✅ Create table directly in MySQL
# States.createTable(ifNotExists=True)