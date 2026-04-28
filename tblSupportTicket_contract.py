from tblSupportTicket_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# GET ALL SUPPORT TICKETS
# =====================================================
def GetAllSupportTickets():
    try:
        tickets = GettblSupportTicket()

        if not tickets:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no support tickets found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": ticket.id,
                "intUserId": ticket.intUserId,
                "nvcharSubject": ticket.nvcharSubject,
                "nvcharMessage": ticket.nvcharMessage,
                "nvcharStatus": ticket.nvcharStatus,
                "dtCreatedDatetime": ticket.dtCreatedDatetime.isoformat() if ticket.dtCreatedDatetime else None
            }
            for ticket in tickets
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "support tickets retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_contract",
            function_name="GetAllSupportTickets",
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
# GET SUPPORT TICKETS BY USER ID
# =====================================================
def GetSupportTicketsByUserId(json_data: dict):
    try:
        user_id = json_data.get('intUserId')
        if not user_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing intUserId",
                    "data": []
                }
            )

        tickets = GettblSupportTicketByUserId(user_id)
        
        if not tickets:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no support tickets found for this user",
                    "data": []
                }
            )

        result_list = [
            {
                "id": ticket.id,
                "intUserId": ticket.intUserId,
                "nvcharSubject": ticket.nvcharSubject,
                "nvcharMessage": ticket.nvcharMessage,
                "nvcharStatus": ticket.nvcharStatus,
                "dtCreatedDatetime": ticket.dtCreatedDatetime.isoformat() if ticket.dtCreatedDatetime else None
            }
            for ticket in tickets
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "support tickets retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_contract",
            function_name="GetSupportTicketsByUserId",
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
# GET SUPPORT TICKET BY ID
# =====================================================
def GetSupportTicketById(json_data: dict):
    try:
        ticket_id = json_data.get('id')
        if not ticket_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        ticket = GettblSupportTicketById(ticket_id)

        if not ticket:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "support ticket not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "support ticket retrieved successfully",
                "data": {
                    "id": ticket.id,
                    "intUserId": ticket.intUserId,
                    "nvcharSubject": ticket.nvcharSubject,
                    "nvcharMessage": ticket.nvcharMessage,
                    "nvcharStatus": ticket.nvcharStatus,
                    "dtCreatedDatetime": ticket.dtCreatedDatetime.isoformat() if ticket.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_contract",
            function_name="GetSupportTicketById",
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
# SAVE SUPPORT TICKET
# =====================================================
def SaveSupportTicket(json_data: dict):
    try:
        ticket = savetblSupportTicket(json_data)

        if not ticket:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save support ticket",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "support ticket saved successfully",
                "data": {
                    "id": ticket.id,
                    "intUserId": ticket.intUserId,
                    "nvcharSubject": ticket.nvcharSubject,
                    "nvcharMessage": ticket.nvcharMessage,
                    "nvcharStatus": ticket.nvcharStatus,
                    "dtCreatedDatetime": ticket.dtCreatedDatetime.isoformat() if ticket.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_contract",
            function_name="SaveSupportTicket",
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
# EDIT SUPPORT TICKET
# =====================================================
def EditSupportTicket(json_data: dict):
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

        ticket = edittblSupportTicket(json_data)

        if not ticket:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit support ticket",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "support ticket updated successfully",
                "data": {
                    "id": ticket.id,
                    "intUserId": ticket.intUserId,
                    "nvcharSubject": ticket.nvcharSubject,
                    "nvcharMessage": ticket.nvcharMessage,
                    "nvcharStatus": ticket.nvcharStatus,
                    "dtCreatedDatetime": ticket.dtCreatedDatetime.isoformat() if ticket.dtCreatedDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_contract",
            function_name="EditSupportTicket",
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
# DELETE SUPPORT TICKET
# =====================================================
def DeleteSupportTicket(json_data: dict):
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

        ticket = deletetblSupportTicket(json_data)

        if not ticket:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "support ticket not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "support ticket deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblSupportTicket_contract",
            function_name="DeleteSupportTicket",
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
