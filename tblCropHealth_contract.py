from tblCropHealthScan_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# VALIDATION
# =====================================================
def validate_crop_health_payload(json_data: dict):
    
    if json_data.get("intHealthScore"):
        try:
            score = int(json_data["intHealthScore"])
            if score < 0 or score > 100:
                return "Health score must be between 0 and 100"
        except:
            return "Invalid health score"
    
    return None


# =====================================================
# GET ALL CROP HEALTH SCANS
# =====================================================
def GettblCropHealthScan1():

    try:

        rows = GettblCropHealthScan()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No crop health scans found",
                    "data": []
                }
            )

        result = []

        for r in rows:
            result.append(jsonable_encoder(to_json(r, r.id)))

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop health scans fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCropHealth_contract",
            function_name="GettblCropHealthScan1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET SCANS BY FARMER
# =====================================================
def GettblCropHealthScanByFarmerId1(json_data: dict):

    try:

        farmer_id = json_data.get("intFarmerId")

        if not farmer_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "intFarmerId is required",
                    "data": []
                }
            )

        rows = GettblCropHealthScanByFarmerId(farmer_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop health scans fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCropHealth_contract",
            function_name="GettblCropHealthScanByFarmerId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# SAVE CROP HEALTH SCAN
# =====================================================
def savetblCropHealthScan1(json_data: dict):

    try:

        validation_error = validate_crop_health_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        scan = savetblCropHealthScan(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop health scan saved successfully",
                "data": jsonable_encoder(to_json(scan, scan.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCropHealth_contract",
            function_name="savetblCropHealthScan1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT CROP HEALTH SCAN
# =====================================================
def edittblCropHealthScan1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        scan = edittblCropHealthScan(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop health scan updated",
                "data": jsonable_encoder(to_json(scan, scan.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCropHealth_contract",
            function_name="edittblCropHealthScan1",
            payload=json_data,
            exc=e
        )


# =====================================================
# DELETE CROP HEALTH SCAN
# =====================================================
def deletetblCropHealthScan1(json_data: dict):

    try:

        scan = deletetblCropHealthScan(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop health scan deleted",
                "data": {"id": scan.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCropHealth_contract",
            function_name="deletetblCropHealthScan1",
            payload=json_data,
            exc=e
        )
