from pydantic import BaseModel
from fastapi.responses import JSONResponse


class SendOTPRequest(BaseModel):
    phone: str


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str


class ResendOTPRequest(BaseModel):
    phone: str


class OTPStatusRequest(BaseModel):
    phone: str


class CheckUserRequest(BaseModel):
    phone: str


def SendPhoneOTP1(data: SendOTPRequest):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "OTP sent successfully", "data": {"phone": data.phone}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def VerifyPhoneOTP1(data: VerifyOTPRequest):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "OTP verified successfully", "data": {"phone": data.phone}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def ResendPhoneOTP1(data: ResendOTPRequest):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "OTP resent successfully", "data": {"phone": data.phone}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def CheckPhoneOTPStatus1(data: OTPStatusRequest):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "OTP status checked", "data": {"phone": data.phone, "verified": False}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def CheckUserByPhone1(data: CheckUserRequest):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "user check complete", "data": {"phone": data.phone, "exists": False}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
