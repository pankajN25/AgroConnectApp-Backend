from tblTransaction_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# GET ALL TRANSACTIONS
# =====================================================
def GetAllTransactions():
    try:
        transactions = GettblTransaction()

        if not transactions:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no transactions found",
                    "data": []
                }
            )

        result_list = [
            {
                "id": transaction.id,
                "intOrderId": transaction.intOrderId,
                "nvcharTransactionNo": transaction.nvcharTransactionNo,
                "floatAmount": transaction.floatAmount,
                "nvcharPaymentMethod": transaction.nvcharPaymentMethod,
                "nvcharPaymentStatus": transaction.nvcharPaymentStatus,
                "dtTransactionDate": transaction.dtTransactionDate.isoformat() if transaction.dtTransactionDate else None
            }
            for transaction in transactions
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "transactions retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblTransaction_contract",
            function_name="GetAllTransactions",
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
# GET TRANSACTIONS BY ORDER ID
# =====================================================
def GetTransactionsByOrderId(json_data: dict):
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

        transactions = GettblTransactionByOrderId(order_id)
        
        if not transactions:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "no transactions found for this order",
                    "data": []
                }
            )

        result_list = [
            {
                "id": transaction.id,
                "intOrderId": transaction.intOrderId,
                "nvcharTransactionNo": transaction.nvcharTransactionNo,
                "floatAmount": transaction.floatAmount,
                "nvcharPaymentMethod": transaction.nvcharPaymentMethod,
                "nvcharPaymentStatus": transaction.nvcharPaymentStatus,
                "dtTransactionDate": transaction.dtTransactionDate.isoformat() if transaction.dtTransactionDate else None
            }
            for transaction in transactions
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "transactions retrieved successfully",
                "data": result_list
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblTransaction_contract",
            function_name="GetTransactionsByOrderId",
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
# GET TRANSACTION BY ID
# =====================================================
def GetTransactionById(json_data: dict):
    try:
        transaction_id = json_data.get('id')
        if not transaction_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Missing id",
                    "data": {}
                }
            )

        transaction = GettblTransactionById(transaction_id)

        if not transaction:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "transaction not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "transaction retrieved successfully",
                "data": {
                    "id": transaction.id,
                    "intOrderId": transaction.intOrderId,
                    "nvcharTransactionNo": transaction.nvcharTransactionNo,
                    "floatAmount": transaction.floatAmount,
                    "nvcharPaymentMethod": transaction.nvcharPaymentMethod,
                    "nvcharPaymentStatus": transaction.nvcharPaymentStatus,
                    "dtTransactionDate": transaction.dtTransactionDate.isoformat() if transaction.dtTransactionDate else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblTransaction_contract",
            function_name="GetTransactionById",
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
# SAVE TRANSACTION
# =====================================================
def SaveTransaction(json_data: dict):
    try:
        transaction = savetblTransaction(json_data)

        if not transaction:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to save transaction",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "transaction saved successfully",
                "data": {
                    "id": transaction.id,
                    "intOrderId": transaction.intOrderId,
                    "nvcharTransactionNo": transaction.nvcharTransactionNo,
                    "floatAmount": transaction.floatAmount,
                    "nvcharPaymentMethod": transaction.nvcharPaymentMethod,
                    "nvcharPaymentStatus": transaction.nvcharPaymentStatus,
                    "dtTransactionDate": transaction.dtTransactionDate.isoformat() if transaction.dtTransactionDate else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblTransaction_contract",
            function_name="SaveTransaction",
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
# EDIT TRANSACTION
# =====================================================
def EditTransaction(json_data: dict):
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

        transaction = edittblTransaction(json_data)

        if not transaction:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Failed to edit transaction",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "transaction updated successfully",
                "data": {
                    "id": transaction.id,
                    "intOrderId": transaction.intOrderId,
                    "nvcharTransactionNo": transaction.nvcharTransactionNo,
                    "floatAmount": transaction.floatAmount,
                    "nvcharPaymentMethod": transaction.nvcharPaymentMethod,
                    "nvcharPaymentStatus": transaction.nvcharPaymentStatus,
                    "dtTransactionDate": transaction.dtTransactionDate.isoformat() if transaction.dtTransactionDate else None
                }
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblTransaction_contract",
            function_name="EditTransaction",
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
# DELETE TRANSACTION
# =====================================================
def DeleteTransaction(json_data: dict):
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

        transaction = deletetblTransaction(json_data)

        if not transaction:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not found",
                    "message": "transaction not found",
                    "data": {}
                }
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "transaction deleted successfully",
                "data": {}
            }
        )

    except Exception as e:
        log_exception(
            file_name="tblTransaction_contract",
            function_name="DeleteTransaction",
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
