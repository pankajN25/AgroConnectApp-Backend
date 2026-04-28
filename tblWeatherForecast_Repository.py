from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================
class tblWeatherForecast(SQLObject):

    intLocationId = BigIntCol(default=None)
    intTemperature = BigIntCol(default=None)
    intMinTemperature = BigIntCol(default=None)
    intMaxTemperature = BigIntCol(default=None)
    intHumidity = BigIntCol(default=None)
    intRainfallProbability = BigIntCol(default=None)
    intRainfallAmount = BigIntCol(default=None)
    intWindSpeed = BigIntCol(default=None)
    nvcharWeatherCondition = StringCol(length=100, default=None)
    nvcharDescription = StringCol(length=500, default=None)
    
    dtForecastDate = DateTimeCol(default=datetime.now)
    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    
    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL WEATHER FORECASTS
# =====================================================
def GettblWeatherForecast():
    try:
        return list(tblWeatherForecast.select(tblWeatherForecast.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblWeatherForecast_Repository",
            function_name="GettblWeatherForecast",
            payload={},
            exc=e
        )
        return []


# =====================================================
# GET WEATHER FORECAST COUNT
# =====================================================
def GettblWeatherForecastCount():
    try:
        count = tblWeatherForecast.select(tblWeatherForecast.q.ynDeleted == False).count()
        return {"totalWeatherForecastCount": count}
    except Exception as e:
        log_exception(
            file_name="tblWeatherForecast_Repository",
            function_name="GettblWeatherForecastCount",
            payload={},
            exc=e
        )
        return {"totalWeatherForecastCount": 0}


# =====================================================
# GET FORECASTS BY LOCATION
# =====================================================
def GettblWeatherForecastByLocationId(intLocationId):
    try:
        row = tblWeatherForecast.select(
            AND(
                tblWeatherForecast.q.intLocationId == intLocationId,
                tblWeatherForecast.q.ynDeleted == False
            )
        )
        return row
    except Exception as e:
        log_exception(
            file_name="tblWeatherForecast_Repository",
            function_name="GettblWeatherForecastByLocationId",
            payload={"intLocationId": intLocationId},
            exc=e
        )
        return []


# =====================================================
# SAVE WEATHER FORECAST
# =====================================================
def savetblWeatherForecast(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblWeatherForecast.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            return tblWeatherForecast(**obj)

    except Exception as e:
        log_exception(
            file_name="tblWeatherForecast_Repository",
            function_name="savetblWeatherForecast",
            payload=obj,
            exc=e
        )
        return None


# =====================================================
# EDIT WEATHER FORECAST
# =====================================================
def edittblWeatherForecast(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        forecast = tblWeatherForecast.get(JsonString['id'])

        forecast.intLocationId = JsonString.get('intLocationId', forecast.intLocationId)
        forecast.intTemperature = JsonString.get('intTemperature', forecast.intTemperature)
        forecast.intMinTemperature = JsonString.get('intMinTemperature', forecast.intMinTemperature)
        forecast.intMaxTemperature = JsonString.get('intMaxTemperature', forecast.intMaxTemperature)
        forecast.intHumidity = JsonString.get('intHumidity', forecast.intHumidity)
        forecast.intRainfallProbability = JsonString.get('intRainfallProbability', forecast.intRainfallProbability)
        forecast.intRainfallAmount = JsonString.get('intRainfallAmount', forecast.intRainfallAmount)
        forecast.intWindSpeed = JsonString.get('intWindSpeed', forecast.intWindSpeed)
        forecast.nvcharWeatherCondition = JsonString.get('nvcharWeatherCondition', forecast.nvcharWeatherCondition)
        forecast.nvcharDescription = JsonString.get('nvcharDescription', forecast.nvcharDescription)

        forecast.dtDateofModification = datetime.now()

        return forecast

    except Exception as e:
        log_exception(
            file_name="tblWeatherForecast_Repository",
            function_name="edittblWeatherForecast",
            payload=JsonString1,
            exc=e
        )
        return None


# =====================================================
# DELETE WEATHER FORECAST
# =====================================================
def deletetblWeatherForecast(JsonString):
    try:
        forecast = tblWeatherForecast.get(JsonString['id'])
        forecast.ynDeleted = True
        return forecast

    except Exception as e:
        log_exception(
            file_name="tblWeatherForecast_Repository",
            function_name="deletetblWeatherForecast",
            payload=JsonString,
            exc=e
        )
        return None


# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblWeatherForecast.createTable(ifNotExists=True)
