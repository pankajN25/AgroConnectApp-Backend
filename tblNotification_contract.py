from tblNotification_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# VALIDATION
# =====================================================
def validate_notification_payload(json_data: dict):
    
    if json_data.get("nvcharTitle"):
        title = str(json_data["nvcharTitle"]).strip()
        if len(title) < 1:
            return "Notification title is required"
    
    return None


# =====================================================
# GET ALL NOTIFICATIONS
# =====================================================
def GettblNotification1():

    try:

        rows = GettblNotification()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No notifications found",
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
                "message": "Notifications fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblNotification_contract",
            function_name="GettblNotification1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET NOTIFICATIONS BY FARMER
# =====================================================
def GettblNotificationByFarmerId1(json_data: dict):

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

        rows = GettblNotificationByFarmerId(farmer_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Notifications fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblNotification_contract",
            function_name="GettblNotificationByFarmerId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# SAVE NOTIFICATION
# =====================================================
def savetblNotification1(json_data: dict):

    try:

        validation_error = validate_notification_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        notification = savetblNotification(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Notification saved successfully",
                "data": jsonable_encoder(to_json(notification, notification.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblNotification_contract",
            function_name="savetblNotification1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT NOTIFICATION
# =====================================================
def edittblNotification1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        notification = edittblNotification(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Notification updated",
                "data": jsonable_encoder(to_json(notification, notification.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblNotification_contract",
            function_name="edittblNotification1",
            payload=json_data,
            exc=e
        )


# =====================================================
# DELETE NOTIFICATION
# =====================================================
def deletetblNotification1(json_data: dict):

    try:

        notification = deletetblNotification(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Notification deleted",
                "data": {"id": notification.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblNotification_contract",
            function_name="deletetblNotification1",
            payload=json_data,
            exc=e
        )
