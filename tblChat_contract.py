from tblChatRoom_Repository import *
from tblChatMessage_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# VALIDATION
# =====================================================
def validate_chat_room_payload(json_data: dict):
    
    if json_data.get("nvcharRoomName"):
        room_name = str(json_data["nvcharRoomName"]).strip()
        if len(room_name) < 1:
            return "Room name is required"
    
    return None


# =====================================================
# GET ALL CHAT ROOMS
# =====================================================
def GettblChatRoom1():

    try:

        rows = GettblChatRoom()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No chat rooms found",
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
                "message": "Chat rooms fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="GettblChatRoom1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# SAVE CHAT ROOM
# =====================================================
def savetblChatRoom1(json_data: dict):

    try:

        validation_error = validate_chat_room_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        room = savetblChatRoom(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Chat room saved successfully",
                "data": jsonable_encoder(to_json(room, room.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="savetblChatRoom1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT CHAT ROOM
# =====================================================
def edittblChatRoom1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        room = edittblChatRoom(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Chat room updated",
                "data": jsonable_encoder(to_json(room, room.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="edittblChatRoom1",
            payload=json_data,
            exc=e
        )


# =====================================================
# DELETE CHAT ROOM
# =====================================================
def deletetblChatRoom1(json_data: dict):

    try:

        room = deletetblChatRoom(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Chat room deleted",
                "data": {"id": room.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="deletetblChatRoom1",
            payload=json_data,
            exc=e
        )


# =====================================================
# GET ALL CHAT MESSAGES
# =====================================================
def GettblChatMessage1():

    try:

        rows = GettblChatMessage()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No chat messages found",
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
                "message": "Chat messages fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="GettblChatMessage1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# SAVE CHAT MESSAGE
# =====================================================
def savetblChatMessage1(json_data: dict):

    try:

        message = savetblChatMessage(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Chat message saved successfully",
                "data": jsonable_encoder(to_json(message, message.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="savetblChatMessage1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT CHAT MESSAGE
# =====================================================
def edittblChatMessage1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        message = edittblChatMessage(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Chat message updated",
                "data": jsonable_encoder(to_json(message, message.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="edittblChatMessage1",
            payload=json_data,
            exc=e
        )


# =====================================================
# DELETE CHAT MESSAGE
# =====================================================
def deletetblChatMessage1(json_data: dict):

    try:

        message = deletetblChatMessage(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Chat message deleted",
                "data": {"id": message.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblChat_contract",
            function_name="deletetblChatMessage1",
            payload=json_data,
            exc=e
        )


# =====================================================
# GET MESSAGES BY ROOM ID
# =====================================================
def GettblChatMessageByChatRoomId1(json_data: dict):
    try:
        room_id = json_data.get("intChatRoomId")
        if not room_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "intChatRoomId is required", "data": []}
            )

        rows = GettblChatMessageByChatRoomId(room_id)
        result = [jsonable_encoder(to_json(r, r.id)) for r in rows if r]

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Messages fetched successfully", "data": result}
        )

    except Exception as e:
        log_exception(file_name="tblChat_contract", function_name="GettblChatMessageByChatRoomId1", payload=json_data, exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})


# =====================================================
# GET CHAT ROOMS BY USER
# =====================================================
def GettblChatRoomByCreatedBy1(json_data: dict):
    try:
        user_id = json_data.get("intCreatedBy")
        if not user_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "intCreatedBy is required", "data": []}
            )

        rows = GettblChatRoomByCreatedBy(user_id)
        result = [jsonable_encoder(to_json(r, r.id)) for r in rows if r]

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Chat rooms fetched successfully", "data": result}
        )

    except Exception as e:
        log_exception(file_name="tblChat_contract", function_name="GettblChatRoomByCreatedBy1", payload=json_data, exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": []})
