from fastapi.responses import JSONResponse


def GoogleCoachLogin1(json_data: dict):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Google coach login successful", "data": json_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def GoogleLogin1(json_data: dict):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Google login successful", "data": json_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})


def GoogleCompleteRegistration1(json_data: dict):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Registration completed", "data": json_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e), "data": {}})
