from tblFarmerRating_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# GET ALL FARMER RATINGS
# =====================================================
def GetAllFarmerRatings():
    try:
        ratings = GettblFarmerRating()

        if not ratings:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no farmer ratings found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": rating.id,
                "intFarmerId": rating.intFarmerId,
                "intUserId": rating.intUserId,
                "floatRating": rating.floatRating,
                "nvcharReview": rating.nvcharReview,
                "dtCreatedDatetime": rating.dtCreatedDatetime.isoformat() if rating.dtCreatedDatetime else None
            }
            for rating in ratings
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer ratings retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_contract",
            function_name="GetAllFarmerRatings",
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
# GET FARMER RATINGS BY FARMER ID
# =====================================================
def GetFarmerRatingsByFarmerId(json_data: dict):
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

        ratings = GettblFarmerRatingByFarmerId(farmer_id)
        
        if not ratings:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no farmer ratings found for this farmer",
                    "data": []
                }
            )

        result_list = [
            {
                "id": rating.id,
                "intFarmerId": rating.intFarmerId,
                "intUserId": rating.intUserId,
                "floatRating": rating.floatRating,
                "nvcharReview": rating.nvcharReview,
                "dtCreatedDatetime": rating.dtCreatedDatetime.isoformat() if rating.dtCreatedDatetime else None
            }
            for rating in ratings
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer ratings retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_contract",
            function_name="GetFarmerRatingsByFarmerId",
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
# GET FARMER RATING BY ID
# =====================================================
def GetFarmerRatingById(json_data: dict):
    try:
        rating_id = json_data.get('id')
        if not rating_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        rating = GettblFarmerRatingById(rating_id)

        if not rating:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "farmer rating not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer rating retrieved successfully",
                "data": {
                    "id": rating.id,
                    "intFarmerId": rating.intFarmerId,
                    "intUserId": rating.intUserId,
                    "floatRating": rating.floatRating,
                    "nvcharReview": rating.nvcharReview,
                    "dtCreatedDatetime": rating.dtCreatedDatetime.isoformat() if rating.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_contract",
            function_name="GetFarmerRatingById",
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
# SAVE FARMER RATING
# =====================================================
def SaveFarmerRating(json_data: dict):
    try:
        rating = savetblFarmerRating(json_data)

        if not rating:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save farmer rating",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer rating saved successfully",
                "data": {
                    "id": rating.id,
                    "intFarmerId": rating.intFarmerId,
                    "intUserId": rating.intUserId,
                    "floatRating": rating.floatRating,
                    "nvcharReview": rating.nvcharReview,
                    "dtCreatedDatetime": rating.dtCreatedDatetime.isoformat() if rating.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_contract",
            function_name="SaveFarmerRating",
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
# EDIT FARMER RATING
# =====================================================
def EditFarmerRating(json_data: dict):
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

        rating = edittblFarmerRating(json_data)

        if not rating:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit farmer rating",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer rating updated successfully",
                "data": {
                    "id": rating.id,
                    "intFarmerId": rating.intFarmerId,
                    "intUserId": rating.intUserId,
                    "floatRating": rating.floatRating,
                    "nvcharReview": rating.nvcharReview,
                    "dtCreatedDatetime": rating.dtCreatedDatetime.isoformat() if rating.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_contract",
            function_name="EditFarmerRating",
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
# DELETE FARMER RATING
# =====================================================
def DeleteFarmerRating(json_data: dict):
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

        rating = deletetblFarmerRating(json_data)

        if not rating:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "farmer rating not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "farmer rating deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerRating_contract",
            function_name="DeleteFarmerRating",
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
