import re
from tkinter import Image
from tblFarmerRegister_Repository import *
from CommonFunction import *
import os
import uuid
from datetime import datetime
from fastapi import UploadFile, File, Form, HTTPException
from PIL import Image
from sqlobject import SQLObjectNotFound
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# VALIDATION
# =====================================================
def validate_payload(json_data: dict):
    if json_data.get("nvcharPhoneNumber"):
        phone = str(json_data["nvcharPhoneNumber"]).strip()

        if not re.fullmatch(r"\d{10}", phone):
            return "Phone number must be 10 digits"

    if json_data.get("nvcharEmail"):
        email = str(json_data["nvcharEmail"]).strip().lower()

        if not re.fullmatch(r"^[a-z0-9][a-z0-9.]*@gmail\.com$", email):
            return "Email must be valid gmail"

    return None


# ================= CONFIG =================
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024

BASE_UPLOAD_DIR = "uploads/tblFarmerRegister"
BASE_URL = "http://127.0.0.1:8000/uploads/tblFarmerRegister"


# ================= HELPERS =================
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_and_optimize_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, format="JPEG", optimize=True, quality=quality)


# ================= UPLOAD IMAGE =================
async def uploadtblFarmerRegisterProfilePictureWithMeta1(
        image: UploadFile = File(...),
        AddGuest_id: int = Form(...)
):
    try:

        if not allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")

        contents = await image.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        try:
            user = tblFarmerRegister.get(AddGuest_id)
        except SQLObjectNotFound:
            raise HTTPException(status_code=404, detail="User not found")

        unique_filename = f"{uuid.uuid4()}.jpg"

        user_dir = os.path.join(BASE_UPLOAD_DIR, f"user_{AddGuest_id}")
        os.makedirs(user_dir, exist_ok=True)

        full_image_path = os.path.join(user_dir, unique_filename)
        temp_path = full_image_path + ".tmp"

        with open(temp_path, "wb") as f:
            f.write(contents)

        resize_and_optimize_image(temp_path, full_image_path)
        os.remove(temp_path)

        image_url = f"{BASE_URL}/user_{AddGuest_id}/{unique_filename}"

        # ✅ Correct column name
        user.nvcharProfilePhotoUrl = image_url
        user.dtDateofModification = datetime.now()

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
# GET ALL FARMERS
# =====================================================
def GettblFarmerRegister1():
    try:

        rows = GettblFarmerRegister()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No farmers found",
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
                "message": "Farmers fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="GettblFarmerRegister1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET BY CITY
# =====================================================
def GettblFarmerRegisterByCityId1(json_data: dict):
    try:

        city_id = json_data.get("intCityId")

        if not city_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "intCityId is required",
                    "data": []
                }
            )

        rows = GettblFarmerRegisterByCityId(city_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Farmers fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="GettblFarmerRegisterByCityId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# GET BY STATE
# =====================================================
def GettblFarmerRegisterByintstateId1(json_data: dict):
    try:

        state_id = json_data.get("intstateId")

        rows = GettblFarmerRegisterByintstateId(state_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Farmers fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="GettblFarmerRegisterByintstateId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# GET BY COUNTRY
# =====================================================
def GettblFarmerRegisterByintcountryId1(json_data: dict):
    try:

        country_id = json_data.get("intcountryId")

        rows = GettblFarmerRegisterByintcountryId(country_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Farmers fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="GettblFarmerRegisterByintcountryId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# SAVE FARMER
# =====================================================
def savetblFarmerRegister1(json_data: dict):
    try:

        validation_error = validate_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        user = savetblFarmerRegister(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Farmer saved successfully",
                "data": jsonable_encoder(to_json(user, user.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="savetblFarmerRegister1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT FARMER
# =====================================================
def edittblFarmerRegister1(json_data: dict):
    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        user = edittblFarmerRegister(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Farmer updated",
                "data": jsonable_encoder(to_json(user, user.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="edittblFarmerRegister1",
            payload=json_data,
            exc=e
        )


def ChangeFarmerPassword1(json_data: dict):
    try:
        farmer_id = json_data.get("id")
        current_password = str(json_data.get("currentPassword") or "")
        new_password = str(json_data.get("newPassword") or "")

        if not farmer_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required", "data": {}}
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

        result = ChangeFarmerPassword(farmer_id, current_password, new_password)

        if not result.get("ok"):
            message = result.get("message") or "Could not change password"
            status_code = 400 if message == "Current password is incorrect" else 404 if message == "Farmer not found" else 500
            return JSONResponse(
                status_code=status_code,
                content={"status": "error", "message": message, "data": {}}
            )

        farmer = result["farmer"]
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Password changed successfully",
                "data": jsonable_encoder(to_json(farmer, farmer.id)),
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="ChangeFarmerPassword1",
            payload=json_data,
            exc=e
        )
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )


# =====================================================
# DELETE
# =====================================================
def deletetblFarmerRegister1(json_data: dict):
    try:

        user = deletetblFarmerRegister(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Farmer deleted",
                "data": {"id": user.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="deletetblFarmerRegister1",
            payload=json_data,
            exc=e
        )


# =====================================================
# PHONE VERIFIED
# =====================================================
def updatephoneverifactionstatus1(json_data: dict):
    try:

        phone = json_data.get("nvcharPhoneNumber")

        users = updatephoneverifactionstatus(phone)

        result = [to_json(u, u.id) for u in users]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Phone verified",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegister_contract",
            function_name="updatephoneverifactionstatus1",
            payload=json_data,
            exc=e
        )
