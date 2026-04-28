from tblFarmerLogin_Repository import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from CommonFunction import log_exception, to_json


# ===============================
# GET ALL
# ===============================
def GettblFarmerLogin1():
    try:

        users = GettblFarmerLogin()

        if not users:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No farmers found",
                    "data": []
                }
            )

        result = [to_json(u, u.id) for u in users]

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
            file_name="tblFarmerLogin_contract",
            function_name="GettblFarmerLogin1",
            payload={},
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


# ===============================
# GET BY ID
# ===============================
def GettblFarmerLoginById1(json_data: dict):
    try:

        user_id = json_data.get("id")

        if not user_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "id is required",
                    "data": {}
                }
            )

        user = GettblFarmerLoginById(user_id)

        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Farmer not found",
                    "data": {}
                }
            )

        result = to_json(user, user.id)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Farmer found",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerLogin_contract",
            function_name="GettblFarmerLoginById1",
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


# ===============================
# LOGIN FLEXIBLE
# ===============================
def GettblFarmerLoginFlexible1(json_data: dict):
    try:

        identifier = json_data.get("identifier")
        password = json_data.get("nvcharPassword")

        if not identifier or not password:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "identifier and nvcharPassword required",
                    "data": []
                }
            )

        users = GettblFarmerLoginFlexible(identifier, password)

        if not users:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Invalid login credentials",
                    "data": []
                }
            )

        result = [to_json(u, u.id) for u in users]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Login successful",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblFarmerLogin_contract",
            function_name="GettblFarmerLoginFlexible1",
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


def UpdateFarmerPassword1(json_data: dict):
    phone = json_data.get("nvcharPhoneNumber")
    password = json_data.get("nvcharPassword")

    UpdateFarmerPassword(phone, password)

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Password updated successfully"
        }
    )


# ===============================
# SAVE
# ===============================
def savetblFarmerLogin1(json_data: dict):
    try:

        user = savetblFarmerLogin(json_data)

        if not user:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Failed to save farmer",
                    "data": {}
                }
            )

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
            file_name="tblFarmerLogin_contract",
            function_name="savetblFarmerLogin1",
            payload=json_data,
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": {}}
        )


# ===============================
# EDIT
# ===============================
def edittblFarmerLogin1(json_data: dict):
    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "id required",
                    "data": {}
                }
            )

        user = edittblFarmerLogin(json_data)

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
            file_name="tblFarmerLogin_contract",
            function_name="edittblFarmerLogin1",
            payload=json_data,
            exc=e
        )


# ===============================
# DELETE
# ===============================
def deletetblFarmerLogin1(json_data: dict):
    try:

        user = deletetblFarmerLogin(json_data)

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
            file_name="tblFarmerLogin_contract",
            function_name="deletetblFarmerLogin1",
            payload=json_data,
            exc=e
        )