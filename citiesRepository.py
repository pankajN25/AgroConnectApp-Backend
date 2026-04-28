import sys
import datetime
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception


class Cities(SQLObject):
    name = StringCol(length=255, default=None)
    state_id = BigIntCol(default=None)
    state_code = StringCol(length=255, default=None)
    country_id = BigIntCol(default=None)
    country_code = StringCol(length=255, default=None)
    latitude = StringCol(length=100, default=None)
    longitude = StringCol(length=100, default=None)
    created_at = DateTimeCol(default=datetime.datetime.now())
    updated_at = DateTimeCol(default=None)
    flag = BigIntCol(default=None)
    wikiDataId = StringCol(length=255, default=None)


def GetCities():
    try:
        return Cities.select()
    except Exception as e:
        log_exception(file_name="citiesRepository", function_name="GetCities", exc=e)


def GetCitiesById(Jid):
    try:
        return Cities.get(Jid)
    except Exception as e:
        log_exception(file_name="citiesRepository", function_name="GetCitiesById", payload={"id": Jid}, exc=e)


def GetCitiesByState_id(state_id):
    try:
        return Cities.select(AND(Cities.q.state_id == state_id))
    except Exception as e:
        log_exception(file_name="citiesRepository", function_name="GetCitiesByState_id", exc=e)


def GetCitiesByState_code(state_code):
    try:
        return Cities.select(AND(Cities.q.state_code == state_code))
    except Exception as e:
        log_exception(file_name="citiesRepository", function_name="GetCitiesByState_code", exc=e)


def GetCitiesByCountry_id(country_id):
    try:
        return Cities.select(AND(Cities.q.country_id == country_id))
    except Exception as e:
        log_exception(file_name="citiesRepository", function_name="GetCitiesByCountry_id", exc=e)


def GetCitiesByCountry_code(country_code):
    try:
        return Cities.select(AND(Cities.q.country_code == country_code))
    except Exception as e:
        log_exception(file_name="citiesRepository", function_name="GetCitiesByCountry_code", exc=e)


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
Cities.createTable(ifNotExists=True)
