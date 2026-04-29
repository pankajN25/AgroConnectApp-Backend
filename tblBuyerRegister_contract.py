from tblBuyerRegister_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile, File, Form, HTTPException
from sqlobject import SQLObjectNotFound
from PIL import Image
import os
import uuid
from datetime import datetime
from pathlib import Path


# =====================================================
# VALIDATION
# =====================================================
def validate_buyer_register_payload(json_data: dict):
    
    # Required fields for registration
    if not json_data.get("nvcharFullName"):
        return "Buyer full name is required"
    
    fullName = str(json_data["nvcharFullName"]).strip()
    if len(fullName) < 1:
        return "Buyer full name cannot be empty"
    
    if not json_data.get("nvcharEmail"):
        return "Buyer email is required"
    
    email = str(json_data["nvcharEmail"]).strip()
    if len(email) < 5:
        return "Buyer email is invalid"
    
    if not json_data.get("nvcharPassword"):
        return "Password is required"
    
    password = str(json_data["nvcharPassword"]).strip()
    if len(password) < 1:
        return "Password cannot be empty"
    
    if json_data.get("nvcharProfilePhotoUrl"):
        profileUrl = str(json_data["nvcharProfilePhotoUrl"]).strip()
        if len(profileUrl) < 1:
            return "Profile photo URL is invalid"
    
    return None


# =====================================================
# HANDLE PROFILE PHOTO UPLOAD
# =====================================================
def handle_profile_photo_upload(file_content, buyer_id, file_extension):
    try:
        upload_dir = f"uploads/tblBuyerRegister/buyer_{buyer_id}"
        Path(upload_dir).mkdir(parents=True, exist_ok=True)
        
        file_name = f"profile_photo.{file_extension}"
        file_path = os.path.join(upload_dir, file_name)
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return file_path
    except Exception as e:
        log_exception(
            file_name="tblBuyerRegister_contract",
            function_name="handle_profile_photo_upload",
            payload={"buyer_id": buyer_id, "file_extension": file_extension},
            exc=e
        )
        return None


# ================= CONFIG =================
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024

BASE_UPLOAD_DIR = "uploads/tblBuyerRegister"
BASE_URL = "http://127.0.0.1:8000/uploads/tblBuyerRegister"


# ================= HELPERS =================
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_and_optimize_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, format="JPEG", optimize=True, quality=quality)


# ================= UPLOAD IMAGE =================
async def uploadtblBuyerRegisterProfilePictureWithMeta1(
        image: UploadFile = File(...),
        buyer_id: int = Form(...)
):
    try:
        if not allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")

        contents = await image.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        try:
            user = tblBuyerRegister.get(buyer_id)
        except SQLObjectNotFound:
            raise HTTPException(status_code=404, detail="Buyer not found")

        unique_filename = f"{uuid.uuid4()}.jpg"

        user_dir = os.path.join(BASE_UPLOAD_DIR, f"user_{buyer_id}")
        os.makedirs(user_dir, exist_ok=True)

        full_image_path = os.path.join(user_dir, unique_filename)
        temp_path = full_image_path + ".tmp"

        with open(temp_path, "wb") as f:
            f.write(contents)

        resize_and_optimize_image(temp_path, full_image_path)
        os.remove(temp_path)

        image_url = f"{BASE_URL}/user_{buyer_id}/{unique_filename}"

        user.nvcharProfilePhotoUrl = image_url
        user.dtModifyDatetime = datetime.now()

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Profile picture uploaded",
                "data": {
                    "id": user.id,
                    "nvcharEmail": user.nvcharEmail,
                    "nvcharFullName": user.nvcharFullName,
                    "nvcharPhoneNumber": user.nvcharPhoneNumber,
                    "nvcharProfilePhotoUrl": user.nvcharProfilePhotoUrl
                }
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# GET ALL BUYERS
# =====================================================
def GettblBuyerRegister1():

    try:

        rows = GettblBuyerRegister()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No buyers found",
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
                "message": "Buyers fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblBuyerRegister_contract",
            function_name="GettblBuyerRegister1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET BUYER BY ID
# =====================================================
def GettblBuyerRegisterById1(json_data: dict):

    try:

        buyer_id = json_data.get("id")

        if not buyer_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "id is required",
                    "data": []
                }
            )

        buyer = GettblBuyerRegisterById(buyer_id)

        if not buyer:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Buyer not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Buyer fetched successfully",
                "data": {
                    "id": buyer.id,
                    "nvcharFullName": buyer.nvcharFullName,
                    "nvcharEmail": buyer.nvcharEmail,
                    "nvcharPhoneNumber": buyer.nvcharPhoneNumber,
                    "nvcharProfilePhotoUrl": buyer.nvcharProfilePhotoUrl,
                    "nvcharCity": buyer.nvcharCity,
                    "nvcharState": buyer.nvcharState,
                    "nvcharCountry": buyer.nvcharCountry,
                    "nvcharAddress": buyer.nvcharAddress,
                    "ynPhoneVerified": buyer.ynPhoneVerified,
                    "dtCreatedDatetime": buyer.dtCreatedDatetime.isoformat() if buyer.dtCreatedDatetime else None,
                }
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblBuyerRegister_contract",
            function_name="GettblBuyerRegisterById1",
            payload=json_data,
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )


# =====================================================
# SAVE BUYER
# =====================================================
def savetblBuyerRegister1(json_data: dict):

    try:

        validation_error = validate_buyer_register_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        buyer = savetblBuyerRegister(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Buyer registered successfully",
                "data": jsonable_encoder(to_json(buyer, buyer.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblBuyerRegister_contract",
            function_name="savetblBuyerRegister1",
            payload=json_data,
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )


# =====================================================
# EDIT BUYER
# =====================================================
def edittblBuyerRegister1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id is required"}
            )

        buyer = edittblBuyerRegister(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Buyer updated successfully",
                "data": jsonable_encoder(to_json(buyer, buyer.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblBuyerRegister_contract",
            function_name="edittblBuyerRegister1",
            payload=json_data,
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )


def ChangeBuyerPassword1(json_data: dict):
    try:
        buyer_id = json_data.get("id")
        current_password = str(json_data.get("currentPassword") or "")
        new_password = str(json_data.get("newPassword") or "")

        if not buyer_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id is required", "data": {}}
            )

        if not current_password or not new_password:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Current password and new password are required",
                    "data": {},
                }
            )

        if len(new_password) < 6:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "New password must be at least 6 characters long",
                    "data": {},
                }
            )

        if current_password == new_password:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "New password must be different from current password",
                    "data": {},
                }
            )

        result = ChangeBuyerPassword(buyer_id, current_password, new_password)

        if not result.get("ok"):
            message = result.get("message") or "Could not change password"
            status_code = 400 if message == "Current password is incorrect" else 404 if message == "Buyer not found" else 500
            return JSONResponse(
                status_code=status_code,
                content={"status": "error", "message": message, "data": {}}
            )

        buyer = result["buyer"]
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Password changed successfully",
                "data": jsonable_encoder(to_json(buyer, buyer.id)),
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblBuyerRegister_contract",
            function_name="ChangeBuyerPassword1",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )


# =====================================================
# DELETE BUYER
# =====================================================
def deletetblBuyerRegister1(json_data: dict):

    try:

        buyer = deletetblBuyerRegister(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Buyer deleted successfully",
                "data": {"id": buyer.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblBuyerRegister_contract",
            function_name="deletetblBuyerRegister1",
            payload=json_data,
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )


# =====================================================
# BUYER LOGIN CONTRACT
# =====================================================
def GettblBuyerLoginFlexible1(json_data: dict):
    try:
        buyer = GettblBuyerLoginFlexible(json_data)

        if buyer:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Login successful",
                    "data": jsonable_encoder(to_json(buyer, buyer.id))
                }
            )
        else:
            return JSONResponse(
                status_code=401,  # 401 means Unauthorized / Bad Password
                content={
                    "status": "error",
                    "message": "Invalid email/phone or password",
                    "data": {}
                }
            )

    except Exception as e:
        log_exception(file_name="tblBuyerRegister_contract", function_name="GettblBuyerLoginFlexible1",
                      payload=json_data, exc=e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )
