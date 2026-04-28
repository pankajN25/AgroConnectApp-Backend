from tblOrder_Repository import *
from CommonFunction import *
import re
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# VALIDATION
# =====================================================
def validate_order_payload(json_data: dict):
    
    if json_data.get("nvcharOrderNumber"):
        order_number = str(json_data["nvcharOrderNumber"]).strip()
        if len(order_number) < 1:
            return "Order number is required"
    
    if json_data.get("intQuantity"):
        try:
            quantity = int(json_data["intQuantity"])
            if quantity <= 0:
                return "Quantity must be greater than 0"
        except:
            return "Invalid quantity"
    
    return None


# =====================================================
# GET ALL ORDERS
# =====================================================
def GettblOrder1():

    try:

        rows = GettblOrder()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No orders found",
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
                "message": "Orders fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblOrder_contract",
            function_name="GettblOrder1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET ORDERS BY FARMER
# =====================================================
def GettblOrderByFarmerId1(json_data: dict):

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

        rows = GettblOrderByFarmerId(farmer_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Orders fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblOrder_contract",
            function_name="GettblOrderByFarmerId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# GET ORDERS BY BUYER
# =====================================================
def GettblOrderByBuyerId1(json_data: dict):

    try:

        buyer_id = json_data.get("intBuyerId")

        rows = GettblOrderByBuyerId(buyer_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Orders fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblOrder_contract",
            function_name="GettblOrderByBuyerId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# SAVE ORDER
# =====================================================
def savetblOrder1(json_data: dict):

    try:

        validation_error = validate_order_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        order = savetblOrder(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Order saved successfully",
                "data": jsonable_encoder(to_json(order, order.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblOrder_contract",
            function_name="savetblOrder1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT ORDER
# =====================================================
def edittblOrder1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        order = edittblOrder(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Order updated",
                "data": jsonable_encoder(to_json(order, order.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblOrder_contract",
            function_name="edittblOrder1",
            payload=json_data,
            exc=e
        )


# =====================================================
# DELETE ORDER
# =====================================================
def deletetblOrder1(json_data: dict):

    try:

        order = deletetblOrder(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Order deleted",
                "data": {"id": order.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblOrder_contract",
            function_name="deletetblOrder1",
            payload=json_data,
            exc=e
        )
