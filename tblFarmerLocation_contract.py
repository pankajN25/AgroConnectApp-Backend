from tblFarmerLocation_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# GET ALL FARMER LOCATIONS
# =====================================================
def GetAllFarmerLocations():
    try:
        locations = GettblFarmerLocation()

        if not locations:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no farmer locations found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": location.id,
                "intFarmerId": location.intFarmerId,
                "floatLatitude": location.floatLatitude,
                "floatLongitude": location.floatLongitude,
                "nvcharAddress": location.nvcharAddress,
                "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
            }
            for location in locations
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer locations retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_contract",
            function_name="GetAllFarmerLocations",
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
# GET FARMER LOCATIONS BY FARMER ID
# =====================================================
def GetFarmerLocationsByFarmerId(json_data: dict):
    try:
        farmer_id = json_data.get('intFarmerId')
        if not farmer_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing intFarmerId",
                    "data": []
                }
            )

        locations = GettblFarmerLocationByFarmerId(farmer_id)
        
        if not locations:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no farmer locations found for this farmer",
                    "data": []
                }
            )

        result_list = [
            {
                "id": location.id,
                "intFarmerId": location.intFarmerId,
                "floatLatitude": location.floatLatitude,
                "floatLongitude": location.floatLongitude,
                "nvcharAddress": location.nvcharAddress,
                "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
            }
            for location in locations
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer locations retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_contract",
            function_name="GetFarmerLocationsByFarmerId",
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
# GET FARMER LOCATION BY ID
# =====================================================
def GetFarmerLocationById(json_data: dict):
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

        location = GettblFarmerLocationById(location_id)

        if not location:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "farmer location not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer location retrieved successfully",
                "data": {
                    "id": location.id,
                    "intFarmerId": location.intFarmerId,
                    "floatLatitude": location.floatLatitude,
                    "floatLongitude": location.floatLongitude,
                    "nvcharAddress": location.nvcharAddress,
                    "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_contract",
            function_name="GetFarmerLocationById",
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
# SAVE FARMER LOCATION
# =====================================================
def SaveFarmerLocation(json_data: dict):
    try:
        location = savetblFarmerLocation(json_data)

        if not location:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save farmer location",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer location saved successfully",
                "data": {
                    "id": location.id,
                    "intFarmerId": location.intFarmerId,
                    "floatLatitude": location.floatLatitude,
                    "floatLongitude": location.floatLongitude,
                    "nvcharAddress": location.nvcharAddress,
                    "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_contract",
            function_name="SaveFarmerLocation",
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
# EDIT FARMER LOCATION
# =====================================================
def EditFarmerLocation(json_data: dict):
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

        location = edittblFarmerLocation(json_data)

        if not location:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit farmer location",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer location updated successfully",
                "data": {
                    "id": location.id,
                    "intFarmerId": location.intFarmerId,
                    "floatLatitude": location.floatLatitude,
                    "floatLongitude": location.floatLongitude,
                    "nvcharAddress": location.nvcharAddress,
                    "dtUpdatedDatetime": location.dtUpdatedDatetime.isoformat() if location.dtUpdatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_contract",
            function_name="EditFarmerLocation",
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
# DELETE FARMER LOCATION
# =====================================================
def DeleteFarmerLocation(json_data: dict):
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

        location = deletetblFarmerLocation(json_data)

        if not location:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "farmer location not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer location deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerLocation_contract",
            function_name="DeleteFarmerLocation",
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
