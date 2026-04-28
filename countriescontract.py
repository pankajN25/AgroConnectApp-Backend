from pydantic_core import to_json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from countriesRepository import *
from CommonFunction import *


def GetCountries1():
    try:
        countries = GetCountries()
        if not countries:
            return JSONResponse(status_code=404, content=jsonable_encoder({"status": "not found", "message": "no countries found", "data": []}))
        result = [to_json(c, c.id) for c in countries]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "countries retrieved successfully", "data": result}))
    except Exception as e:
        log_exception(file_name="countriescontract", function_name="GetCountries1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetCountriesById1(json_data: dict):
    try:
        country_id = json_data.get("id")
        country = GetCountriesById(country_id)
        if not country:
            return JSONResponse(status_code=404, content=jsonable_encoder({"status": "not found", "message": "country not found", "data": {}}))
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "country found", "data": to_json(country, country.id)}))
    except Exception as e:
        log_exception(file_name="countriescontract", function_name="GetCountriesById1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def GetCountriesByPhonecode1(json_data: dict):
    try:
        phonecode = json_data.get("phonecode")
        countries = GetCountriesByPhonecode(phonecode)
        result = [to_json(c, c.id) for c in countries if c]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "countries found", "data": result}))
    except Exception as e:
        log_exception(file_name="countriescontract", function_name="GetCountriesByPhonecode1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetCountriesByRegion_id1(json_data: dict):
    try:
        region_id = json_data.get("region_id")
        countries = GetCountriesByRegion_id(region_id)
        result = [to_json(c, c.id) for c in countries if c]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "countries found", "data": result}))
    except Exception as e:
        log_exception(file_name="countriescontract", function_name="GetCountriesByRegion_id1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})
