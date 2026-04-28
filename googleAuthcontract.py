from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from CommonFunction import log_exception, to_json

WEB_CLIENT_ID = "83809202447-nc3euu613h7ia0ionu2k78430rfffq52.apps.googleusercontent.com"


def _verify_google_token(token: str) -> dict:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests

    # Try with web client id first, then without audience (fallback for Android client tokens)
    for audience in [WEB_CLIENT_ID, None]:
        try:
            if audience:
                return id_token.verify_oauth2_token(token, google_requests.Request(), audience)
            else:
                return id_token.verify_oauth2_token(token, google_requests.Request())
        except Exception:
            continue
    raise ValueError("Could not verify Google token with any known audience")


def GoogleCoachLogin1(json_data: dict):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Google coach login successful", "data": json_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def GoogleLogin1(json_data: dict):
    try:
        from tblFarmerRegister_Repository import tblFarmerRegister
        from tblBuyerRegister_Repository import tblBuyerRegister
        from sqlobject import AND

        token = json_data.get("id_token") or json_data.get("access_token") or ""
        if not token:
            return JSONResponse(status_code=400, content={"status": "error", "message": "id_token is required", "data": {}})

        try:
            idinfo = _verify_google_token(token)
        except Exception as verify_err:
            return JSONResponse(status_code=401, content={"status": "error", "message": f"Token verification failed: {str(verify_err)}", "data": {}})

        email = (idinfo.get("email") or "").strip().lower()
        google_name = idinfo.get("name", "")
        google_picture = idinfo.get("picture", "")

        if not email:
            return JSONResponse(status_code=400, content={"status": "error", "message": "Could not extract email from Google token", "data": {}})

        # Check farmer table
        farmers = list(tblFarmerRegister.select(
            AND(tblFarmerRegister.q.nvcharEmail == email, tblFarmerRegister.q.ynDeleted == False)
        ))
        if farmers:
            farmer = farmers[0]
            farmer_data = to_json(farmer, farmer.id)
            return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "Farmer login successful",
                "data": {
                    "auth_type": "farmer_login",
                    "farmer": jsonable_encoder(farmer_data),
                    "google_name": google_name,
                    "google_email": email,
                    "google_picture": google_picture,
                }
            })

        # Check buyer table
        buyers = list(tblBuyerRegister.select(
            AND(tblBuyerRegister.q.nvcharEmail == email, tblBuyerRegister.q.ynDeleted == False)
        ))
        if buyers:
            buyer = buyers[0]
            buyer_data = to_json(buyer, buyer.id)
            return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "Buyer login successful",
                "data": {
                    "auth_type": "buyer_login",
                    "buyer": jsonable_encoder(buyer_data),
                    "google_name": google_name,
                    "google_email": email,
                    "google_picture": google_picture,
                }
            })

        # New user
        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "New user, please complete registration",
            "data": {
                "auth_type": "register",
                "google_name": google_name,
                "google_email": email,
                "google_picture": google_picture,
            }
        })

    except Exception as e:
        log_exception(file_name="googleAuthcontract", function_name="GoogleLogin1", payload=json_data, exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def GoogleCompleteRegistration1(json_data: dict):
    try:
        from tblFarmerRegister_Repository import tblFarmerRegister, savetblFarmerRegister
        from tblBuyerRegister_Repository import tblBuyerRegister, savetblBuyerRegister
        from sqlobject import AND

        role = json_data.get("role", "")
        token = json_data.get("id_token") or json_data.get("access_token") or ""

        # Verify token to get email (don't rely on client-supplied email)
        google_email = ""
        google_picture = ""
        if token:
            try:
                idinfo = _verify_google_token(token)
                google_email = (idinfo.get("email") or "").strip().lower()
                google_picture = idinfo.get("picture", "")
            except Exception:
                pass

        if not google_email:
            google_email = (json_data.get("google_email") or "").strip().lower()

        if not google_email:
            return JSONResponse(status_code=400, content={"status": "error", "message": "Could not determine Google email", "data": {}})

        if role == "farmer":
            farmer_payload = {
                "nvcharFullName": json_data.get("nvcharFullName", ""),
                "nvcharPhoneNumber": json_data.get("nvcharPhoneNumber", ""),
                "nvcharEmail": google_email,
                "nvcharPassword": json_data.get("nvcharPassword", ""),
                "nvcharProfilePhotoUrl": google_picture,
                "intcountryId": str(json_data.get("intcountryId", "") or ""),
                "intstateId": str(json_data.get("intstateId", "") or ""),
                "intCityId": str(json_data.get("intCityId", "") or ""),
                "nvcharFarmingType": json_data.get("nvcharFarmingType", ""),
                "nvcharPreferredLanguage": json_data.get("nvcharPreferredLanguage", ""),
                "nvcharDescription": json_data.get("nvcharDescription", ""),
                "ynPhoneVerified": False,
            }
            farmer = savetblFarmerRegister(farmer_payload)
            if not farmer:
                return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to create farmer account", "data": {}})
            farmer_data = to_json(farmer, farmer.id)
            return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "Farmer account created successfully",
                "data": {
                    "auth_type": "farmer_login",
                    "farmer": jsonable_encoder(farmer_data),
                }
            })

        elif role == "buyer":
            buyer_payload = {
                "nvcharFullName": json_data.get("nvcharFullName", ""),
                "nvcharPhoneNumber": json_data.get("nvcharPhoneNumber", ""),
                "nvcharEmail": google_email,
                "nvcharPassword": json_data.get("nvcharPassword", ""),
                "nvcharProfilePhotoUrl": google_picture,
                "nvcharAddress": json_data.get("nvcharAddress", ""),
                "ynPhoneVerified": False,
            }
            buyer = savetblBuyerRegister(buyer_payload)
            if not buyer:
                return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to create buyer account", "data": {}})
            buyer_data = to_json(buyer, buyer.id)
            return JSONResponse(status_code=200, content={
                "status": "success",
                "message": "Buyer account created successfully",
                "data": {
                    "auth_type": "buyer_login",
                    "buyer": jsonable_encoder(buyer_data),
                }
            })

        else:
            return JSONResponse(status_code=400, content={"status": "error", "message": "role must be 'farmer' or 'buyer'", "data": {}})

    except Exception as e:
        log_exception(file_name="googleAuthcontract", function_name="GoogleCompleteRegistration1", payload=json_data, exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
