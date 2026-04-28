from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from mstCropQualityGrade_Repository import *
from CommonFunction import *


def GetmstCropQualityGrade1():
    try:
        rows = GetmstCropQualityGrade()
        result = [to_json(r, r.id) for r in rows]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "quality grades retrieved", "data": result}))
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_contract", function_name="GetmstCropQualityGrade1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def savemstCropQualityGrade1(json_data: dict):
    try:
        row = savemstCropQualityGrade(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to save", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "quality grade saved", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_contract", function_name="savemstCropQualityGrade1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def editmstCropQualityGrade1(json_data: dict):
    try:
        row = editmstCropQualityGrade(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to update", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "quality grade updated", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_contract", function_name="editmstCropQualityGrade1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def deletemstCropQualityGrade1(json_data: dict):
    try:
        row = deletemstCropQualityGrade(json_data)
        if not row:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to delete", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "quality grade deleted", "data": to_json(row, row.id)}))
    except Exception as e:
        log_exception(file_name="mstCropQualityGrade_contract", function_name="deletemstCropQualityGrade1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
