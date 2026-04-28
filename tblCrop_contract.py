from tblCrop_Repository import *
from CommonFunction import *
import re
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile, File, Form, HTTPException
import os
import uuid
from datetime import datetime




# =====================================================
# IMAGE UPLOAD CONFIG
# =====================================================

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024

UPLOAD_DIR = "uploads/crops"
BASE_URL = "http://127.0.0.1:8000/uploads/crops"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =====================================================
# UPLOAD CROP IMAGE
# =====================================================
async def uploadCropImage1(
        image: UploadFile = File(...),
        crop_id: int = Form(...)
):

    try:

        if not allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")

        contents = await image.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        try:
            crop = tblCrop.get(crop_id)
        except:
            raise HTTPException(status_code=404, detail="Crop not found")

        unique_filename = f"{uuid.uuid4()}.jpg"

        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        image_url = f"{BASE_URL}/{unique_filename}"

        crop.set(
            nvcharCropImageUrl=image_url,
            dtDateofModification=datetime.now()
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop image uploaded",
                "data": {
                    "crop_id": crop.id,
                    "image_url": image_url
                }
            }
        )

    except HTTPException:
        raise

    except Exception as e:

        log_exception(
            file_name="tblCrop_contract",
            function_name="uploadCropImage1",
            payload={"crop_id": crop_id},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )
        
        
# =====================================================
# VALIDATION
# =====================================================
def validate_crop_payload(json_data: dict):

    if not json_data.get("nvcharCropName"):
        return "Crop name is required"

    if not json_data.get("floatQuantity"):
        return "Quantity is required"

    if not json_data.get("floatPricePerKg"):
        return "Price per kg is required"

    return None


# =====================================================
# GET ALL CROPS
# =====================================================
def GettblCrop1():

    try:

        rows = GettblCrop()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No crops found",
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
                "message": "Crops fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCrop_contract",
            function_name="GettblCrop1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET CROPS BY FARMER ID
# =====================================================
def GettblCropByFarmerId1(json_data: dict):
    try:
        farmer_id = json_data.get("intFarmerId")
        if not farmer_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "intFarmerId is required", "data": []}
            )

        rows = GettblCropByFarmerId(int(farmer_id))

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"{len(rows)} crops found",
                "data": jsonable_encoder(rows)
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCrop_contract",
            function_name="GettblCropByFarmerId1",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET CROPS BY CATEGORY
# =====================================================
def GettblCropByCategoryId1(json_data: dict):

    try:

        category_id = json_data.get("intCropCategoryId")

        if not category_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "intCropCategoryId is required",
                    "data": []
                }
            )

        rows = GettblCropByCategoryId(category_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crops fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCrop_contract",
            function_name="GettblCropByCategoryId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# SAVE CROP
# =====================================================
def savetblCrop1(json_data: dict):

    try:

        validation_error = validate_crop_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        # Normalize harvest date to a real date object for SQLObject DateCol
        harvest_date = json_data.get("dtHarvestDate")
        if isinstance(harvest_date, str) and harvest_date.strip():
            try:
                json_data["dtHarvestDate"] = datetime.strptime(
                    harvest_date.strip(), "%Y-%m-%d"
                ).date()
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "message": "dtHarvestDate must be in YYYY-MM-DD format",
                        "data": {}
                    }
                )

        crop = savetblCrop(json_data)

        if not crop:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save crop. Please check your data.",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop saved successfully",
                "data": jsonable_encoder(to_json(crop, crop.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCrop_contract",
            function_name="savetblCrop1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT CROP
# =====================================================
def edittblCrop1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        crop = edittblCrop(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop updated",
                "data": jsonable_encoder(to_json(crop, crop.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCrop_contract",
            function_name="edittblCrop1",
            payload=json_data,
            exc=e
        )


# =====================================================
# DELETE CROP
# =====================================================
def deletetblCrop1(json_data: dict):

    try:

        crop = deletetblCrop(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop deleted",
                "data": {"id": crop.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblCrop_contract",
            function_name="deletetblCrop1",
            payload=json_data,
            exc=e
        )
