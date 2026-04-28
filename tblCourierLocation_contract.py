from tblCourierLocation_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


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
