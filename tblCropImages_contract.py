from tblCropImages_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import uuid
from datetime import datetime
from fastapi import UploadFile, File, Form, HTTPException
from PIL import Image
from sqlobject import SQLObjectNotFound


# ================= CONFIG =================
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024

BASE_UPLOAD_DIR = "uploads/tblCropImages"
BASE_URL = "http://127.0.0.1:8000/uploads/tblCropImages"


# ================= HELPERS =================
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_and_optimize_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, format="JPEG", optimize=True, quality=quality)


# ================= UPLOAD CROP IMAGE =================
async def uploadtblCropImageWithMeta(
        image: UploadFile = File(...),
        intCropId: int = Form(...)
):
    try:

        if not allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")

        contents = await image.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        try:
            # Verify crop exists
            from tblCrop_Repository import tblCrop
            crop = tblCrop.get(intCropId)
        except SQLObjectNotFound:
            raise HTTPException(status_code=404, detail="Crop not found")

        unique_filename = f"{uuid.uuid4()}.jpg"

        crop_dir = os.path.join(BASE_UPLOAD_DIR, f"crop_{intCropId}")
        os.makedirs(crop_dir, exist_ok=True)

        full_image_path = os.path.join(crop_dir, unique_filename)
        temp_path = full_image_path + ".tmp"

        with open(temp_path, "wb") as f:
            f.write(contents)

        resize_and_optimize_image(temp_path, full_image_path)
        os.remove(temp_path)

        image_url = f"{BASE_URL}/crop_{intCropId}/{unique_filename}"

        # ✅ Correct column name
        image_obj = savetblCropImages({
            "intCropId": intCropId,
            "nvcharImageUrl": image_url,
            "ynPrimary": False
        })

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Crop image uploaded",
                "data": {
                    "id": image_obj.id,
                    "intCropId": image_obj.intCropId,
                    "nvcharImageUrl": image_obj.nvcharImageUrl,
                    "ynPrimary": image_obj.ynPrimary
                }
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# GET ALL CROP IMAGES
# =====================================================
def GetAllCropImages():
    try:
        images = GettblCropImages()

        if not images:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no crop images found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": image.id,
                "intCropId": image.intCropId,
                "nvcharImageUrl": image.nvcharImageUrl,
                "ynPrimary": image.ynPrimary,
                "dtCreatedDatetime": image.dtCreatedDatetime.isoformat() if image.dtCreatedDatetime else None
            }
            for image in images
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "crop images retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCropImages_contract",
            function_name="GetAllCropImages",
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
# GET CROP IMAGES BY CROP ID
# =====================================================
def GetCropImagesByCropId(json_data: dict):
    try:
        crop_id = json_data.get('intCropId')
        if not crop_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing intCropId",
                    "data": []
                }
            )

        images = GettblCropImagesByCropId(crop_id)
        
        if not images:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no crop images found for this crop",
                    "data": []
                }
            )

        result_list = [
            {
                "id": image.id,
                "intCropId": image.intCropId,
                "nvcharImageUrl": image.nvcharImageUrl,
                "ynPrimary": image.ynPrimary,
                "dtCreatedDatetime": image.dtCreatedDatetime.isoformat() if image.dtCreatedDatetime else None
            }
            for image in images
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "crop images retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCropImages_contract",
            function_name="GetCropImagesByCropId",
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
# GET CROP IMAGE BY ID
# =====================================================
def GetCropImageById(json_data: dict):
    try:
        image_id = json_data.get('id')
        if not image_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        image = GettblCropImagesById(image_id)

        if not image:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "crop image not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "crop image retrieved successfully",
                "data": {
                    "id": image.id,
                    "intCropId": image.intCropId,
                    "nvcharImageUrl": image.nvcharImageUrl,
                    "ynPrimary": image.ynPrimary,
                    "dtCreatedDatetime": image.dtCreatedDatetime.isoformat() if image.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCropImages_contract",
            function_name="GetCropImageById",
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
# SAVE CROP IMAGE
# =====================================================
def SaveCropImage(json_data: dict):
    try:
        image = savetblCropImages(json_data)

        if not image:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save crop image",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "crop image saved successfully",
                "data": {
                    "id": image.id,
                    "intCropId": image.intCropId,
                    "nvcharImageUrl": image.nvcharImageUrl,
                    "ynPrimary": image.ynPrimary,
                    "dtCreatedDatetime": image.dtCreatedDatetime.isoformat() if image.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCropImages_contract",
            function_name="SaveCropImage",
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
# EDIT CROP IMAGE
# =====================================================
def EditCropImage(json_data: dict):
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

        image = edittblCropImages(json_data)

        if not image:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit crop image",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "crop image updated successfully",
                "data": {
                    "id": image.id,
                    "intCropId": image.intCropId,
                    "nvcharImageUrl": image.nvcharImageUrl,
                    "ynPrimary": image.ynPrimary,
                    "dtCreatedDatetime": image.dtCreatedDatetime.isoformat() if image.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCropImages_contract",
            function_name="EditCropImage",
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
# DELETE CROP IMAGE
# =====================================================
def DeleteCropImage(json_data: dict):
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

        image = deletetblCropImages(json_data)

        if not image:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "crop image not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "crop image deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblCropImages_contract",
            function_name="DeleteCropImage",
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
