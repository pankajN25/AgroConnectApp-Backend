from tblFavoriteCrop_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# GET ALL FAVORITE CROPS
# =====================================================
def GetAllFavoriteCrops():
    try:
        favorites = GettblFavoriteCrop()

        if not favorites:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no favorite crops found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": favorite.id,
                "intUserId": favorite.intUserId,
                "intCropId": favorite.intCropId,
                "dtCreatedDatetime": favorite.dtCreatedDatetime.isoformat() if favorite.dtCreatedDatetime else None
            }
            for favorite in favorites
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "favorite crops retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_contract",
            function_name="GetAllFavoriteCrops",
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
# GET FAVORITE CROPS BY USER ID
# =====================================================
def GetFavoriteCropsByUserId(json_data: dict):
    try:
        user_id = json_data.get('intUserId')
        if not user_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing intUserId",
                    "data": []
                }
            )

        favorites = GettblFavoriteCropByUserId(user_id)
        
        if not favorites:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no favorite crops found for this user",
                    "data": []
                }
            )

        result_list = [
            {
                "id": favorite.id,
                "intUserId": favorite.intUserId,
                "intCropId": favorite.intCropId,
                "dtCreatedDatetime": favorite.dtCreatedDatetime.isoformat() if favorite.dtCreatedDatetime else None
            }
            for favorite in favorites
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "favorite crops retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_contract",
            function_name="GetFavoriteCropsByUserId",
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
# GET FAVORITE CROP BY ID
# =====================================================
def GetFavoriteCropById(json_data: dict):
    try:
        favorite_id = json_data.get('id')
        if not favorite_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        favorite = GettblFavoriteCropById(favorite_id)

        if not favorite:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "favorite crop not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "favorite crop retrieved successfully",
                "data": {
                    "id": favorite.id,
                    "intUserId": favorite.intUserId,
                    "intCropId": favorite.intCropId,
                    "dtCreatedDatetime": favorite.dtCreatedDatetime.isoformat() if favorite.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_contract",
            function_name="GetFavoriteCropById",
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
# SAVE FAVORITE CROP
# =====================================================
def SaveFavoriteCrop(json_data: dict):
    try:
        favorite = savetblFavoriteCrop(json_data)

        if not favorite:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save favorite crop",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "favorite crop saved successfully",
                "data": {
                    "id": favorite.id,
                    "intUserId": favorite.intUserId,
                    "intCropId": favorite.intCropId,
                    "dtCreatedDatetime": favorite.dtCreatedDatetime.isoformat() if favorite.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_contract",
            function_name="SaveFavoriteCrop",
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
# EDIT FAVORITE CROP
# =====================================================
def EditFavoriteCrop(json_data: dict):
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

        favorite = edittblFavoriteCrop(json_data)

        if not favorite:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit favorite crop",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "favorite crop updated successfully",
                "data": {
                    "id": favorite.id,
                    "intUserId": favorite.intUserId,
                    "intCropId": favorite.intCropId,
                    "dtCreatedDatetime": favorite.dtCreatedDatetime.isoformat() if favorite.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_contract",
            function_name="EditFavoriteCrop",
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
# DELETE FAVORITE CROP
# =====================================================
def DeleteFavoriteCrop(json_data: dict):
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

        favorite = deletetblFavoriteCrop(json_data)

        if not favorite:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "favorite crop not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "favorite crop deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFavoriteCrop_contract",
            function_name="DeleteFavoriteCrop",
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
