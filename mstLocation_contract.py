from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from mstLocation_Repository import *
from CommonFunction import *


def GetmstLocation1():
    try:
        rows = GetmstLocation()
        result = [to_json(r, r.id) for r in rows]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "locations retrieved", "data": result}))
    except Exception as e:
        log_exception(file_name="mstLocation_contract", function_name="GetmstLocation1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetmstLocationByCityId1(json_data: dict):
    try:
        city_id = json_data.get("intCityId")
        rows = GetmstLocationByCityId(city_id)
        result = [to_json(r, r.id) for r in rows]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "locations found", "data": result}))
    except Exception as e:
        log_exception(file_name="mstLocation_contract", function_name="GetmstLocationByCityId1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def savemstLocation1(json_data: dict):
    try:
        row = savemstLocation(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to save", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "location saved", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstLocation_contract", function_name="savemstLocation1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def editmstLocation1(json_data: dict):
    try:
        row = editmstLocation(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to update", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "location updated", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstLocation_contract", function_name="editmstLocation1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def deletemstLocation1(json_data: dict):
    try:
        row = deletemstLocation(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to delete", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "location deleted", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstLocation_contract", function_name="deletemstLocation1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
