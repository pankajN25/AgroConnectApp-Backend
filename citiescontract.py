from pydantic_core import to_json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from citiesRepository import *
from CommonFunction import *


def GetCities1():
    try:
        cities = GetCities()
        if not cities:
            return JSONResponse(status_code=404, content=jsonable_encoder({"status": "not found", "message": "no cities found", "data": []}))
        result = [to_json(c, c.id) for c in cities]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "cities retrieved successfully", "data": result}))
    except Exception as e:
        log_exception(file_name="citiescontract", function_name="GetCities1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetCitiesById1(json_data: dict):
    try:
        city_id = json_data.get("id")
        city = GetCitiesById(city_id)
        if not city:
            return JSONResponse(status_code=404, content=jsonable_encoder({"status": "not found", "message": "city not found", "data": {}}))
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "city found", "data": to_json(city, city.id)}))
    except Exception as e:
        log_exception(file_name="citiescontract", function_name="GetCitiesById1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def GetCitiesByState_id1(json_data: dict):
    try:
        state_id = json_data.get("state_id")
        cities = GetCitiesByState_id(state_id)
        result = [to_json(c, c.id) for c in cities if c]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "cities found", "data": result}))
    except Exception as e:
        log_exception(file_name="citiescontract", function_name="GetCitiesByState_id1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetCitiesByState_code1(json_data: dict):
    try:
        state_code = json_data.get("state_code")
        cities = GetCitiesByState_code(state_code)
        result = [to_json(c, c.id) for c in cities if c]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "cities found", "data": result}))
    except Exception as e:
        log_exception(file_name="citiescontract", function_name="GetCitiesByState_code1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetCitiesByCountry_id1(json_data: dict):
    try:
        country_id = json_data.get("country_id")
        cities = GetCitiesByCountry_id(country_id)
        result = [to_json(c, c.id) for c in cities if c]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "cities found", "data": result}))
    except Exception as e:
        log_exception(file_name="citiescontract", function_name="GetCitiesByCountry_id1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetCitiesByCountry_code1(json_data: dict):
    try:
        country_code = json_data.get("country_code")
        cities = GetCitiesByCountry_code(country_code)
        result = [to_json(c, c.id) for c in cities if c]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "cities found", "data": result}))
    except Exception as e:
        log_exception(file_name="citiescontract", function_name="GetCitiesByCountry_code1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})
