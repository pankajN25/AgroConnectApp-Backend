from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from tblDirectMessage_Repository import *
from CommonFunction import *


def send_direct_message1(json_data: dict):
    try:
        # Frontend sends: sender_id / receiver_id / message
        # Model columns:  intSenderId / intReceiverId / nvcharMessage
        payload = {
            "intSenderId":   json_data.get("sender_id") or json_data.get("intSenderId"),
            "intReceiverId": json_data.get("receiver_id") or json_data.get("intReceiverId"),
            "nvcharMessage": json_data.get("message") or json_data.get("nvcharMessage"),
        }
        if not payload["intSenderId"] or not payload["intReceiverId"] or not payload["nvcharMessage"]:
            return JSONResponse(status_code=400, content={"status": "error", "message": "sender_id, receiver_id and message are required", "data": {}})
        msg = savetblDirectMessage(payload)
        if not msg:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to send message", "data": {}})
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "message sent", "data": to_json(msg, msg.id)}))
    except Exception as e:
        log_exception(file_name="direct_message_contract", function_name="send_direct_message1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def get_direct_messages_between_users1(json_data: dict):
    try:
        sender_id = json_data.get("sender_id")
        receiver_id = json_data.get("receiver_id")
        messages = GettblDirectMessageByUsers(sender_id, receiver_id)
        result = [to_json(m, m.id) for m in messages if m]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "messages retrieved", "data": result}))
    except Exception as e:
        log_exception(file_name="direct_message_contract", function_name="get_direct_messages_between_users1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


def get_direct_messages_by_user1(json_data: dict):
    try:
        user_id = json_data.get("user_id")
        messages = GettblDirectMessageByUser(user_id)
        result = [to_json(m, m.id) for m in messages if m]
        return JSONResponse(status_code=200, content=jsonable_encoder({"status": "success", "message": "messages retrieved", "data": result}))
    except Exception as e:
        log_exception(file_name="direct_message_contract", function_name="get_direct_messages_by_user1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})
