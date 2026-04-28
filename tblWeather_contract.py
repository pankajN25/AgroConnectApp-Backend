from tblWeatherForecast_Repository import *
from CommonFunction import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# =====================================================
# VALIDATION
# =====================================================
def validate_weather_payload(json_data: dict):
    
    if json_data.get("intLocationId"):
        try:
            location_id = int(json_data["intLocationId"])
            if location_id <= 0:
                return "Invalid location ID"
        except:
            return "Invalid location ID"
    
    return None


# =====================================================
# GET ALL WEATHER FORECASTS
# =====================================================
def GettblWeatherForecast1():

    try:

        rows = GettblWeatherForecast()

        if not rows:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No weather forecasts found",
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
                "message": "Weather forecasts fetched successfully",
                "data": result
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblWeather_contract",
            function_name="GettblWeatherForecast1",
            payload={},
            exc=e
        )

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "data": []}
        )


# =====================================================
# GET FORECASTS BY LOCATION
# =====================================================
def GettblWeatherForecastByLocationId1(json_data: dict):

    try:

        location_id = json_data.get("intLocationId")

        if not location_id:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "intLocationId is required",
                    "data": []
                }
            )

        rows = GettblWeatherForecastByLocationId(location_id)

        result = [to_json(r, r.id) for r in rows]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Weather forecasts fetched successfully",
                "data": jsonable_encoder(result)
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblWeather_contract",
            function_name="GettblWeatherForecastByLocationId1",
            payload=json_data,
            exc=e
        )


# =====================================================
# SAVE WEATHER FORECAST
# =====================================================
def savetblWeatherForecast1(json_data: dict):

    try:

        validation_error = validate_weather_payload(json_data)

        if validation_error:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": validation_error,
                    "data": {}
                }
            )

        forecast = savetblWeatherForecast(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Weather forecast saved successfully",
                "data": jsonable_encoder(to_json(forecast, forecast.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblWeather_contract",
            function_name="savetblWeatherForecast1",
            payload=json_data,
            exc=e
        )


# =====================================================
# EDIT WEATHER FORECAST
# =====================================================
def edittblWeatherForecast1(json_data: dict):

    try:

        if not json_data.get("id"):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "id required"}
            )

        forecast = edittblWeatherForecast(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Weather forecast updated",
                "data": jsonable_encoder(to_json(forecast, forecast.id))
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblWeather_contract",
            function_name="edittblWeatherForecast1",
            payload=json_data,
            exc=e
        )


# =====================================================
# DELETE WEATHER FORECAST
# =====================================================
def deletetblWeatherForecast1(json_data: dict):

    try:

        forecast = deletetblWeatherForecast(json_data)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Weather forecast deleted",
                "data": {"id": forecast.id}
            }
        )

    except Exception as e:

        log_exception(
            file_name="tblWeather_contract",
            function_name="deletetblWeatherForecast1",
            payload=json_data,
            exc=e
        )
