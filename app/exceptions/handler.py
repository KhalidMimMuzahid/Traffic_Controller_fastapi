# from typing import Any, Callable, Optional
# from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
# from sqlalchemy.exc import SQLAlchemyError


from exceptions.models import CustomError

def create_exception_handler( error_data: CustomError):

    async def exception_handler(request: Request, exc: CustomError):

        return JSONResponse(
             status_code=exc.status_code,
            content={
            is_success: False,
            "error": {
                "message": exc.message,
                "resolution": exc.resolution or "No resolution provided",
            }
        })

    return exception_handler


def register_all_errors(app: FastAPI):
    @app.exception_handler(CustomError)
    async def database__error(request, exc):
        # print(str(exc))
        return JSONResponse(
            content={
                "message":exc.message,
                "error_code": "server_errorxx",
            },
            status_code=exc.status_code,
        )