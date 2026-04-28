from tblOrderStatus_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# GET ALL ORDER STATUS
# =====================================================
def GetAllOrderStatus():
    try:
        statuses = GettblOrderStatus()

        if not statuses:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no order status found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": status.id,
                "intOrderId": status.intOrderId,
                "nvcharStatus": status.nvcharStatus,
                "nvcharDescription": status.nvcharDescription,
                "dtStatusDatetime": status.dtStatusDatetime.isoformat() if status.dtStatusDatetime else None
            }
            for status in statuses
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "order status retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_contract",
            function_name="GetAllOrderStatus",
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
# GET ORDER STATUS BY ORDER ID
# =====================================================
def GetOrderStatusByOrderId(json_data: dict):
    try:
        order_id = json_data.get('intOrderId')
        if not order_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing intOrderId",
                    "data": []
                }
            )

        statuses = GettblOrderStatusByOrderId(order_id)
        
        if not statuses:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no order status found for this order",
                    "data": []
                }
            )

        result_list = [
            {
                "id": status.id,
                "intOrderId": status.intOrderId,
                "nvcharStatus": status.nvcharStatus,
                "nvcharDescription": status.nvcharDescription,
                "dtStatusDatetime": status.dtStatusDatetime.isoformat() if status.dtStatusDatetime else None
            }
            for status in statuses
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "order status retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_contract",
            function_name="GetOrderStatusByOrderId",
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
# GET ORDER STATUS BY ID
# =====================================================
def GetOrderStatusById(json_data: dict):
    try:
        status_id = json_data.get('id')
        if not status_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        status = GettblOrderStatusById(status_id)

        if not status:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "order status not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "order status retrieved successfully",
                "data": {
                    "id": status.id,
                    "intOrderId": status.intOrderId,
                    "nvcharStatus": status.nvcharStatus,
                    "nvcharDescription": status.nvcharDescription,
                    "dtStatusDatetime": status.dtStatusDatetime.isoformat() if status.dtStatusDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_contract",
            function_name="GetOrderStatusById",
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
# SAVE ORDER STATUS
# =====================================================
def SaveOrderStatus(json_data: dict):
    try:
        status = savetblOrderStatus(json_data)

        if not status:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save order status",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "order status saved successfully",
                "data": {
                    "id": status.id,
                    "intOrderId": status.intOrderId,
                    "nvcharStatus": status.nvcharStatus,
                    "nvcharDescription": status.nvcharDescription,
                    "dtStatusDatetime": status.dtStatusDatetime.isoformat() if status.dtStatusDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_contract",
            function_name="SaveOrderStatus",
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
# EDIT ORDER STATUS
# =====================================================
def EditOrderStatus(json_data: dict):
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

        status = edittblOrderStatus(json_data)

        if not status:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit order status",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "order status updated successfully",
                "data": {
                    "id": status.id,
                    "intOrderId": status.intOrderId,
                    "nvcharStatus": status.nvcharStatus,
                    "nvcharDescription": status.nvcharDescription,
                    "dtStatusDatetime": status.dtStatusDatetime.isoformat() if status.dtStatusDatetime else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_contract",
            function_name="EditOrderStatus",
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
# DELETE ORDER STATUS
# =====================================================
def DeleteOrderStatus(json_data: dict):
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

        status = deletetblOrderStatus(json_data)

        if not status:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "order status not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "order status deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblOrderStatus_contract",
            function_name="DeleteOrderStatus",
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
