import sys
import datetime
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception


class Countries(SQLObject):
    name = StringCol(length=100, default=None)
    iso3 = StringCol(length=50, default=None)
    numeric_code = StringCol(length=50, default=None)
    iso2 = StringCol(length=50, default=None)
    phonecode = StringCol(length=255, default=None)
    capital = StringCol(length=255, default=None)
    currency = StringCol(length=255, default=None)
    currency_name = StringCol(length=255, default=None)
    currency_symbol = StringCol(length=255, default=None)
    tld = StringCol(length=255, default=None)
    native = StringCol(length=255, default=None)
    region = StringCol(length=255, default=None)
    region_id = BigIntCol(default=None)
    subregion = StringCol(length=255, default=None)
    subregion_id = BigIntCol(default=None)
    nationality = StringCol(length=255, default=None)
    timezones = StringCol(length=500, default=None)
    translations = StringCol(length=500, default=None)
    latitude = FloatCol(default=None)
    longitude = FloatCol(default=None)
    emoji = StringCol(length=255, default=None)
    emojiU = StringCol(length=255, default=None)
    created_at = DateTimeCol(default=datetime.datetime.now())
    updated_at = DateTimeCol(default=None)
    flag = BigIntCol(default=None)
    wikiDataId = StringCol(length=50, default=None)


def GetCountries():
    try:
        return Countries.select()
    except Exception as e:
        log_exception(file_name="countriesRepository", function_name="GetCountries", exc=e)


def GetCountriesById(Jid):
    try:
        return Countries.get(Jid)
    except Exception as e:
        log_exception(file_name="countriesRepository", function_name="GetCountriesById", payload={"id": Jid}, exc=e)


def GetCountriesByPhonecode(phonecode):
    try:
        return Countries.select(AND(Countries.q.phonecode == phonecode))
    except Exception as e:
        log_exception(file_name="countriesRepository", function_name="GetCountriesByPhonecode", exc=e)


def GetCountriesByRegion_id(region_id):
    try:
        return Countries.select(AND(Countries.q.region_id == region_id))
    except Exception as e:
        log_exception(file_name="countriesRepository", function_name="GetCountriesByRegion_id", exc=e)


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
Countries.createTable(ifNotExists=True)
