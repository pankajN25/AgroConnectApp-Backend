
from pydantic_core import to_json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from statesRepository import *
from CommonFunction import *

def GetStates1():
    try:
        states = GetStates()
        if not states:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "status": "not found",
                    "message": "no states found",
                    "data": []
                })
            )

        result_list = [to_json(state, state.id) for state in states]
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                "status": "success",
                "message": "states retrieved successfully",
                "data": result_list
            })
        )
    except Exception as e:
        log_exception(
            file_name="tblStateContract",
            function_name="GetStates1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404

def GetStatesById1(json_data: dict):
    try:
        state_id = json_data.get("id")
        if not state_id:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "status": "error",
                    "message": 'Missing "id"',
                    "data": {}
                })
            )

        state = GetStatesById(state_id)
        if not state:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "status": "not found",
                    "message": "state not found",
                    "data": {}
                })
            )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                "status": "success",
                "message": "state found",
                "data": to_json(state, state.id)
            })
        )
    except Exception as e:
        log_exception(
            file_name="tblStateContract",
            function_name="GetStatesById1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404

def GetStatesByCountry_id1(json_data: dict):
    try:
        country_id = json_data.get("country_id")
        if not country_id:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "status": "error",
                    "message": 'Missing "country_id"',
                    "data": []
                })
            )

        states = GetStatesByCountry_id(country_id)
        result_list = [to_json(state, state.id) for state in states if state]

        if not result_list:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "status": "not found",
                    "message": "no states found for this country ID",
                    "data": []
                })
            )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                "status": "success",
                "message": "states found",
                "data": result_list
            })
        )

    except Exception as e:
        log_exception(
            file_name="tblStateContract",
            function_name="GetStatesByCountry_id1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404

def GetStatesByCountry_code1(json_data: dict):
    try:
        country_code = json_data.get("country_code")
        if not country_code:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "status": "error",
                    "message": 'Missing "country_code"',
                    "data": []
                })
            )

        states = GetStatesByCountry_code(country_code)
        result_list = [to_json(state, state.id) for state in states if state]

        if not result_list:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "status": "not found",
                    "message": "no states found for this country_code",
                    "data": []
                })
            )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                "status": "success",
                "message": "states found",
                "data": result_list
            })
        )

    except Exception as e:
        log_exception(
            file_name="tblStateContract",
            function_name="GetStatesByCountry_code1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404