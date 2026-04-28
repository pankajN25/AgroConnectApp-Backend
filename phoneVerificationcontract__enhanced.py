import os
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from phoneVerificationsRepository_enhanced import (
    CreatePhoneVerification, VerifyOTPCode, CanResendOTP,
    UpdateTwilioSID, IncrementResendCount, format_phone_number
)
from CommonFunction import log_exception


# ── Pydantic models ──────────────────────────────────────────
class SendOTPRequest(BaseModel):
    phone: Optional[str] = None
    phone_number: Optional[str] = None   # some apps send phone_number

class VerifyOTPRequest(BaseModel):
    phone: Optional[str] = None
    phone_number: Optional[str] = None
    otp: Optional[str] = None
    otp_code: Optional[str] = None       # some apps send otp_code

class ResendOTPRequest(BaseModel):
    phone: Optional[str] = None
    phone_number: Optional[str] = None

class OTPStatusRequest(BaseModel):
    phone: Optional[str] = None
    phone_number: Optional[str] = None

class CheckUserRequest(BaseModel):
    phone: Optional[str] = None
    phone_number: Optional[str] = None


# ── Twilio SMS sender ────────────────────────────────────────
def _send_otp_via_twilio(to_number: str, otp_code: str) -> dict:
    try:
        from twilio.rest import Client
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
        auth_token  = os.environ.get("TWILIO_AUTH_TOKEN", "")
        from_number = os.environ.get("TWILIO_PHONE_NUMBER", "")

        if not account_sid or not auth_token or not from_number:
            return {'success': False, 'error': 'Twilio env vars not set (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)'}

        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=f"Your AgroConnect OTP is: {otp_code}\nValid for 5 minutes. Do not share.",
            from_=from_number,
            to=to_number
        )
        return {'success': True, 'sid': msg.sid}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _get_phone(data) -> str:
    return (data.phone or data.phone_number or "").strip()


# ── Contract functions ───────────────────────────────────────
def SendPhoneOTP1(data: SendOTPRequest):
    try:
        phone = _get_phone(data)
        if not phone:
            return JSONResponse(status_code=400, content={"status": "error", "message": "phone number is required", "data": {}})

        formatted = format_phone_number(phone)

        if not CanResendOTP(formatted):
            return JSONResponse(status_code=429, content={"status": "error", "message": "Please wait 1 minute before requesting another OTP", "data": {}})

        verification = CreatePhoneVerification(formatted)
        if not verification:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to create OTP record", "data": {}})

        sms = _send_otp_via_twilio(formatted, verification.otpcode)
        if not sms['success']:
            return JSONResponse(status_code=500, content={"status": "error", "message": f"Failed to send OTP SMS: {sms['error']}", "data": {}})

        if 'sid' in sms:
            UpdateTwilioSID(verification.id, sms['sid'])

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "OTP sent successfully",
            "data": {"phone": formatted, "expires_in": "5 minutes"}
        })

    except Exception as e:
        log_exception(file_name="phoneVerificationcontract__enhanced", function_name="SendPhoneOTP1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def VerifyPhoneOTP1(data: VerifyOTPRequest):
    try:
        phone = _get_phone(data)
        otp   = (data.otp or data.otp_code or "").strip()

        if not phone:
            return JSONResponse(status_code=400, content={"status": "error", "message": "phone number is required", "data": {}})
        if not otp:
            return JSONResponse(status_code=400, content={"status": "error", "message": "otp is required", "data": {}})

        result = VerifyOTPCode(phone, otp)

        if result['success']:
            return JSONResponse(status_code=200, content={
                "status": "success",
                "message": result['message'],
                "data": {"phone": result.get('phone', phone), "verified": True}
            })
        else:
            return JSONResponse(status_code=400, content={
                "status": "error",
                "message": result['message'],
                "data": {"verification_status": result.get('status'), "attempts_remaining": result.get('attempts_remaining', 0)}
            })

    except Exception as e:
        log_exception(file_name="phoneVerificationcontract__enhanced", function_name="VerifyPhoneOTP1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def ResendPhoneOTP1(data: ResendOTPRequest):
    try:
        phone = _get_phone(data)
        if not phone:
            return JSONResponse(status_code=400, content={"status": "error", "message": "phone number is required", "data": {}})

        formatted = format_phone_number(phone)

        if not CanResendOTP(formatted):
            return JSONResponse(status_code=429, content={"status": "error", "message": "Please wait 1 minute before resending OTP", "data": {}})

        verification = CreatePhoneVerification(formatted)
        if not verification:
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to create OTP record", "data": {}})

        sms = _send_otp_via_twilio(formatted, verification.otpcode)
        if not sms['success']:
            return JSONResponse(status_code=500, content={"status": "error", "message": f"Failed to resend OTP: {sms['error']}", "data": {}})

        if 'sid' in sms:
            UpdateTwilioSID(verification.id, sms['sid'])
        IncrementResendCount(formatted)

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "OTP resent successfully",
            "data": {"phone": formatted, "expires_in": "5 minutes"}
        })

    except Exception as e:
        log_exception(file_name="phoneVerificationcontract__enhanced", function_name="ResendPhoneOTP1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def CheckPhoneOTPStatus1(data: OTPStatusRequest):
    try:
        phone = _get_phone(data)
        if not phone:
            return JSONResponse(status_code=400, content={"status": "error", "message": "phone number is required", "data": {}})
        formatted = format_phone_number(phone)
        from phoneVerificationsRepository_enhanced import GetPendingByPhone
        v = GetPendingByPhone(formatted)
        status = v.otp_status if v else "NO_PENDING"
        return JSONResponse(status_code=200, content={"status": "success", "message": "Status retrieved", "data": {"phone": formatted, "otp_status": status}})
    except Exception as e:
        log_exception(file_name="phoneVerificationcontract__enhanced", function_name="CheckPhoneOTPStatus1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def CheckUserByPhone1(data: CheckUserRequest):
    try:
        phone = _get_phone(data)
        if not phone:
            return JSONResponse(status_code=400, content={"status": "error", "message": "phone number is required", "data": {}})

        formatted = format_phone_number(phone)

        from tblFarmerRegister_Repository import tblFarmerRegister
        from tblBuyerRegister_Repository import tblBuyerRegister
        from sqlobject import OR

        farmers = list(tblFarmerRegister.select(AND(
            tblFarmerRegister.q.nvcharPhoneNumber == phone,
            tblFarmerRegister.q.ynDeleted == False
        )))
        buyers = list(tblBuyerRegister.select(AND(
            tblBuyerRegister.q.nvcharPhoneNumber == phone,
            tblBuyerRegister.q.ynDeleted == False
        )))

        exists = bool(farmers or buyers)
        user_type = "farmer" if farmers else ("buyer" if buyers else None)

        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "User check complete",
            "data": {"phone": formatted, "exists": exists, "user_type": user_type}
        })

    except Exception as e:
        log_exception(file_name="phoneVerificationcontract__enhanced", function_name="CheckUserByPhone1", exc=e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
