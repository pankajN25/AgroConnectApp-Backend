import sys
import datetime
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception


class Regions(SQLObject):
    name = StringCol(length=100, default=None)
    translations = StringCol(length=500, default=None)
    created_at = DateTimeCol(default=datetime.datetime.now())
    updated_at = DateTimeCol(default=None)
    flag = BigIntCol(default=None)
    wikiDataId = StringCol(length=50, default=None)


def GetRegions():
    try:
        return Regions.select()
    except Exception as e:
        log_exception(file_name="regionsRepository", function_name="GetRegions", exc=e)


def GetRegionsById(Jid):
    try:
        return Regions.get(Jid)
    except Exception as e:
        log_exception(file_name="regionsRepository", function_name="GetRegionsById", payload={"id": Jid}, exc=e)


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
Regions.createTable(ifNotExists=True)
