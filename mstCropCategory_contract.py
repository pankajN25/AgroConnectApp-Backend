from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from mstCropCategory_Repository import *
from CommonFunction import *


def GetmstCropCategory1():
    try:
        rows = GetmstCropCategory()
        result = [to_json(r, r.id) for r in rows]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "crop categories retrieved", "data": result}))
    except Exception as e:
        log_exception(file_name="mstCropCategory_contract", function_name="GetmstCropCategory1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def savemstCropCategory1(json_data: dict):
    try:
        row = savemstCropCategory(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to save", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "crop category saved", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstCropCategory_contract", function_name="savemstCropCategory1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def editmstCropCategory1(json_data: dict):
    try:
        row = editmstCropCategory(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to update", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "crop category updated", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstCropCategory_contract", function_name="editmstCropCategory1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def deletemstCropCategory1(json_data: dict):
    try:
        row = deletemstCropCategory(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to delete", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "crop category deleted", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstCropCategory_contract", function_name="deletemstCropCategory1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
