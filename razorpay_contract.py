import os
import hmac
import hashlib
import uuid
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def _get_razorpay_client():
    import razorpay
    key_id = os.environ.get("RAZORPAY_KEY_ID", "")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    if not key_id or not key_secret:
        raise ValueError("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables are not set on Railway")
    return razorpay.Client(auth=(key_id, key_secret))


# =====================================================
# CREATE RAZORPAY ORDER
# =====================================================
def create_razorpay_order(json_data: dict):
    try:
        key_id = os.environ.get("RAZORPAY_KEY_ID", "")
        client = _get_razorpay_client()

        # Frontend already sends amount in paise — do NOT multiply by 100 again
        amount = int(float(json_data.get("amount", 0)))
        if amount <= 0:
            return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid amount", "data": {}})

        order = client.order.create({
            "amount": amount,
            "currency": json_data.get("currency", "INR"),
            "receipt": json_data.get("receipt", ""),
            "notes": json_data.get("notes", {}),
            "payment_capture": 1,
        })
        # Include keyId so frontend can open Razorpay checkout without hardcoding the key
        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "Razorpay order created",
            "data": {**order, "keyId": key_id},
        })

    except ValueError as ve:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(ve), "data": {}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


# =====================================================
# VERIFY PAYMENT + SAVE ORDER TO DB
# =====================================================
def verify_payment_and_create_order(json_data: dict):
    try:
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
        if not key_secret:
            return JSONResponse(status_code=500, content={"status": "error", "message": "RAZORPAY_KEY_SECRET not set on Railway", "data": {}})

        razorpay_order_id  = json_data.get("razorpay_order_id", "")
        razorpay_payment_id = json_data.get("razorpay_payment_id", "")
        razorpay_signature  = json_data.get("razorpay_signature", "")

        # Verify signature
        body = f"{razorpay_order_id}|{razorpay_payment_id}"
        expected_signature = hmac.new(
            key_secret.encode("utf-8"),
            body.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        if expected_signature != razorpay_signature:
            return JSONResponse(status_code=400, content={"status": "error", "message": "Payment signature verification failed", "data": {}})

        # Save order to DB
        # Frontend sends order fields nested inside { order: { intFarmerId, ... } }
        from tblOrder_Repository import savetblOrder
        from CommonFunction import to_json

        order_src = json_data.get("order") or json_data
        order_payload = {
            "intFarmerId":           order_src.get("intFarmerId"),
            "intCropId":             order_src.get("intCropId"),
            "intBuyerId":            order_src.get("intBuyerId"),
            "intQuantity":           order_src.get("intQuantity"),
            "intUnitPrice":          order_src.get("intUnitPrice"),
            "intTotalPrice":         order_src.get("intTotalPrice"),
            "nvcharDeliveryAddress": order_src.get("nvcharDeliveryAddress", ""),
            "nvcharOrderNumber":     razorpay_order_id,
            # Use "Pending" so the farmer sees it in the Pending tab.
            # Payment status is tracked separately in tblTransaction.
            "nvcharStatus":          "Pending",
        }
        saved_order = savetblOrder(order_payload)

        if not saved_order:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Payment verified but failed to save order", "data": {}})

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "Payment verified and order saved successfully",
            "data": jsonable_encoder(to_json(saved_order, saved_order.id))
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


# =====================================================
# COD ORDER — Save directly, no payment needed
# =====================================================
def create_cod_order(json_data: dict):
    try:
        from tblOrder_Repository import savetblOrder
        from CommonFunction import to_json

        # Frontend wraps order fields inside { order: { intFarmerId, ... } }
        order_src = json_data.get("order") or json_data
        order_payload = {
            "intFarmerId":           order_src.get("intFarmerId"),
            "intCropId":             order_src.get("intCropId"),
            "intBuyerId":            order_src.get("intBuyerId"),
            "intQuantity":           order_src.get("intQuantity"),
            "intUnitPrice":          order_src.get("intUnitPrice"),
            "intTotalPrice":         order_src.get("intTotalPrice"),
            "nvcharDeliveryAddress": order_src.get("nvcharDeliveryAddress", ""),
            "nvcharOrderNumber":     order_src.get("nvcharOrderNumber") or f"COD-{uuid.uuid4().hex[:8].upper()}",
            # Use "Pending" so the farmer sees it in the Pending tab.
            "nvcharStatus":          "Pending",
        }
        saved_order = savetblOrder(order_payload)

        if not saved_order:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to place COD order", "data": {}})

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "COD order placed successfully",
            "data": jsonable_encoder(to_json(saved_order, saved_order.id))
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


# =====================================================
# UPDATE ORDER STATUS
# =====================================================
def update_order_status_with_history(json_data: dict):
    try:
        from tblOrder_Repository import tblOrder
        from CommonFunction import to_json

        order_id = json_data.get("id")
        new_status = json_data.get("nvcharStatus")

        if not order_id or not new_status:
            return JSONResponse(status_code=400, content={"status": "error", "message": "id and nvcharStatus are required", "data": {}})

        order = tblOrder.get(order_id)
        order.nvcharStatus = new_status

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": f"Order status updated to {new_status}",
            "data": jsonable_encoder(to_json(order, order.id))
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


# =====================================================
# CANCEL ORDER + RAZORPAY REFUND
# =====================================================
def cancel_order_and_refund(json_data: dict):
    try:
        from tblOrder_Repository import tblOrder
        from CommonFunction import to_json

        order_id = json_data.get("id")
        payment_id = json_data.get("razorpay_payment_id", "")

        if not order_id:
            return JSONResponse(status_code=400, content={"status": "error", "message": "id is required", "data": {}})

        order = tblOrder.get(order_id)
        order.nvcharStatus = "cancelled"

        # Try to refund via Razorpay if payment_id is provided
        refund_data = {}
        if payment_id:
            try:
                client = _get_razorpay_client()
                refund = client.payment.refund(payment_id, {
                    "amount": int(float(order.intTotalPrice or 0)) * 100,
                    "notes": {"reason": json_data.get("reason", "Order cancelled by user")}
                })
                refund_data = refund
            except Exception as refund_err:
                refund_data = {"refund_error": str(refund_err)}

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "Order cancelled",
            "data": {
                "order": jsonable_encoder(to_json(order, order.id)),
                "refund": refund_data
            }
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
