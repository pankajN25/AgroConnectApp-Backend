from tblCourierLocation_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# UPSERT — Update or create the live location for an order
# =====================================================
def UpdateLiveCourierLocation(json_data: dict):
    try:
        order_id = json_data.get("intOrderId")
        lat = json_data.get("floatLatitude")
        lon = json_data.get("floatLongitude")

        if not order_id or lat is None or lon is None:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "intOrderId, floatLatitude and floatLongitude are required", "data": {}}
            )

        loc = UpsertCourierLocationByOrderId(int(order_id), float(lat), float(lon))
        if not loc:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Failed to update courier location", "data": {}}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Courier location updated",
                "data": {
                    "id": loc.id,
                    "intOrderId": loc.intOrderId,
                    "floatLatitude": loc.floatLatitude,
                    "floatLongitude": loc.floatLongitude,
                    "dtUpdatedDatetime": loc.dtUpdatedDatetime.isoformat() if loc.dtUpdatedDatetime else None,
                }
            }
        )
    except Exception as e:
        log_exception("tblCourierLocation_contract", "UpdateLiveCourierLocation", json_data, e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


# =====================================================
# GET LATEST LOCATION — Returns the single current position for an order
# =====================================================
def GetLatestCourierLocation(json_data: dict):
    try:
        order_id = json_data.get("intOrderId")
        if not order_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "intOrderId is required", "data": {}}
            )

        loc = GetLatestCourierLocationByOrderId(int(order_id))
        if not loc:
            return JSONResponse(
                status_code=404,
                content={"status": "not found", "message": "No location found for this order", "data": {}}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Latest courier location retrieved",
                "data": {
                    "id": loc.id,
                    "intOrderId": loc.intOrderId,
                    "floatLatitude": loc.floatLatitude,
                    "floatLongitude": loc.floatLongitude,
                    "dtUpdatedDatetime": loc.dtUpdatedDatetime.isoformat() if loc.dtUpdatedDatetime else None,
                }
            }
        )
    except Exception as e:
        log_exception("tblCourierLocation_contract", "GetLatestCourierLocation", json_data, e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


# =====================================================
# GET ALL COURIER LOCATIONS
# =====================================================
def GetAllCourierLocations():
    try:
        locations = GettblCourierLocation()

        if not locations:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no courier locations found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": location.id,
                "intOrderId": location.intOrderId,
                "floatLatitude": location.floatLatitude,
                "floatLongitude": location.floatLongitude,
                "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
            }
            for location in locations
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "courier locations retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_contract",
            function_name="GetAllCourierLocations",
            payload=None,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "data": []
            }
        )


# =====================================================
# GET COURIER LOCATIONS BY ORDER ID
# =====================================================
def GetCourierLocationsByOrderId(json_data: dict):
    try:
        order_id = json_data.get('intOrderId')
        if not order_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing intOrderId",
                    "data": []
                }
            )

        locations = GettblCourierLocationByOrderId(order_id)
        
        if not locations:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no courier locations found for this order",
                    "data": []
                }
            )

        result_list = [
            {
                "id": location.id,
                "intOrderId": location.intOrderId,
                "floatLatitude": location.floatLatitude,
                "floatLongitude": location.floatLongitude,
                "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
            }
            for location in locations
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "courier locations retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_contract",
            function_name="GetCourierLocationsByOrderId",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "data": []
            }
        )


# =====================================================
# GET COURIER LOCATION BY ID
# =====================================================
def GetCourierLocationById(json_data: dict):
    try:
        location_id = json_data.get('id')
        if not location_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        location = GettblCourierLocationById(location_id)

        if not location:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "courier location not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "courier location retrieved successfully",
                "data": {
                    "id": location.id,
                    "intOrderId": location.intOrderId,
                    "floatLatitude": location.floatLatitude,
                    "floatLongitude": location.floatLongitude,
                    "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_contract",
            function_name="GetCourierLocationById",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "data": {}
            }
        )


# =====================================================
# SAVE COURIER LOCATION
# =====================================================
def SaveCourierLocation(json_data: dict):
    try:
        location = savetblCourierLocation(json_data)

        if not location:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save courier location",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "courier location saved successfully",
                "data": {
                    "id": location.id,
                    "intOrderId": location.intOrderId,
                    "floatLatitude": location.floatLatitude,
                    "floatLongitude": location.floatLongitude,
                    "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_contract",
            function_name="SaveCourierLocation",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "data": {}
            }
        )


# =====================================================
# EDIT COURIER LOCATION
# =====================================================
def EditCourierLocation(json_data: dict):
    try:
        if not json_data.get('id'):
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        location = edittblCourierLocation(json_data)

        if not location:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit courier location",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "courier location updated successfully",
                "data": {
                    "id": location.id,
                    "intOrderId": location.intOrderId,
                    "floatLatitude": location.floatLatitude,
                    "floatLongitude": location.floatLongitude,
                    "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_contract",
            function_name="EditCourierLocation",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "data": {}
            }
        )


# =====================================================
# DELETE COURIER LOCATION
# =====================================================
def DeleteCourierLocation(json_data: dict):
    try:
        if not json_data.get('id'):
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        location = deletetblCourierLocation(json_data)

        if not location:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "courier location not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "courier location deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCourierLocation_contract",
            function_name="DeleteCourierLocation",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "data": {}
            }
        )
