from fastapi.responses import JSONResponse


def create_razorpay_order(json_data: dict):
    try:
        import razorpay, os
        client = razorpay.Client(auth=(os.environ.get("RAZORPAY_KEY_ID"), os.environ.get("RAZORPAY_KEY_SECRET")))
        amount = int(float(json_data.get("amount", 0)) * 100)
        order = client.order.create({"amount": amount, "currency": "INR", "payment_capture": 1})
        return JSONResponse(status_code=200, content={"status": "success", "message": "order created", "data": order})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def verify_payment_and_create_order(json_data: dict):
    try:
        import razorpay, os, hmac, hashlib
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
        razorpay_order_id = json_data.get("razorpay_order_id", "")
        razorpay_payment_id = json_data.get("razorpay_payment_id", "")
        razorpay_signature = json_data.get("razorpay_signature", "")
        body = f"{razorpay_order_id}|{razorpay_payment_id}"
        expected = hmac.new(key_secret.encode(), body.encode(), hashlib.sha256).hexdigest()
        if expected == razorpay_signature:
            return JSONResponse(status_code=200, content={"status": "success", "message": "payment verified", "data": json_data})
        return JSONResponse(status_code=400, content={"status": "error", "message": "payment verification failed", "data": {}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def create_cod_order(json_data: dict):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "COD order placed successfully", "data": json_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def update_order_status_with_history(json_data: dict):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "order status updated", "data": json_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def cancel_order_and_refund(json_data: dict):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "order cancelled", "data": json_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
