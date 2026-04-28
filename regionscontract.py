from pydantic_core import to_json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from regionsRepository import *
from CommonFunction import *


def GetRegions1():
    try:
        regions = GetRegions()
        if not regions:
            return JSONResponse(status_code=404, content=jsonable_encoder({"status": "not found", "message": "no regions found", "data": []}))
        result = [to_json(r, r.id) for r in regions]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "regions retrieved successfully", "data": result}))
    except Exception as e:
        log_exception(file_name="regionscontract", function_name="GetRegions1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def GetRegionsById1(json_data: dict):
    try:
        region_id = json_data.get("id")
        region = GetRegionsById(region_id)
        if not region:
            return JSONResponse(status_code=404, content=jsonable_encoder({"status": "not found", "message": "region not found", "data": {}}))
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "region found", "data": to_json(region, region.id)}))
    except Exception as e:
        log_exception(file_name="regionscontract", function_name="GetRegionsById1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
