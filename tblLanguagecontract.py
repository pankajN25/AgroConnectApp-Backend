
from pydantic_core import to_json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from tblLanguageRepository import *
from CommonFunction import *
def GettableLanguage1():
    try:
        user_list = GettableLanguage()
        if not user_list:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    'status': 'not found',
                    'message': 'no languages found',
                    'data': []
                })
            )

        result_list = [to_json(user, user.id) for user in user_list]
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                'status': 'success',
                'message': 'languages retrieved successfully',
                'data': result_list
            })
        )

    except Exception as e:
        log_exception(
            file_name="tblLanguageContract",
            function_name="GettableLanguage1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404


def GettblLanguageById1(json_data: dict):
    try:
        user_id = json_data.get('id')
        if not user_id:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({'status': 'error', 'message': 'Missing "id"', 'data': {}})
            )

        user = GettblLanguageById(user_id)
        if not user:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({'status': 'not found', 'message': 'Language not found', 'data': {}})
            )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({'status': 'success', 'message': 'Language found', 'data': to_json(user, user.id)})
        )

    except Exception as e:
        log_exception(
            file_name="tblLanguageContract",
            function_name="GettblLanguageById1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404

def savetblLanguage1(json_data: dict):
    try:
        saved_user = savetblLanguage(json_data)
        if not saved_user:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({'status': 'error', 'message': 'Save Language failed', 'data': {}})
            )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                'status': 'success',
                'message': 'Language saved',
                'data': to_json(saved_user, saved_user.id)
            })
        )
    except Exception as e:
        log_exception(
            file_name="tblLanguageContract",
            function_name="savetblLanguage1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404


def edittblLanguage1(json_data: dict):
    try:
        updated_user = edittblLanguage(json_data)
        if not updated_user:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({'status': 'error', 'message': 'Update failed Language', 'data': {}})
            )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({'status': 'success', 'message': 'Language updated', 'data': to_json(updated_user, updated_user.id)})
        )

    except Exception as e:
        log_exception(
            file_name="tblLanguageContract",
            function_name="edittblLanguage1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404
def deletetblLanguage1(json_data: dict):
    try:
        deleted_user = deletetblLanguage(json_data)
        if not deleted_user:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({'status': 'error', 'message': 'Delete failed Language', 'data': {}})
            )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({'status': 'success', 'message': 'Language deleted', 'data': to_json(deleted_user, deleted_user.id)})
        )

    except Exception as e:
        log_exception(
            file_name="tblLanguageContract",
            function_name="deletetblLanguage1",
            payload=request.get_json(silent=True),
            exc=e
        )
        return JSONResponse({
            'status': 'error',
            'message': str(e),
            'data': []
        }), 404
