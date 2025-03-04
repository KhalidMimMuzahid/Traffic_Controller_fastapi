from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
from fastapi import FastAPI, Request, status
from sqlalchemy.exc import SQLAlchemyError
from exceptions.models import CustomError, ExceptionContent
import re
def register_all_errors(app: FastAPI):
    # Handling CustomError 
    @app.exception_handler(CustomError)
    async def database__error(request, exc):
        content = ExceptionContent(message= exc.message, resolution= exc.resolution or "No resolution provided",).to_dict()
        return JSONResponse(
            content=content,
            status_code=exc.status_code,
        )

    # # Handling SQLAlchemyError
    @app.exception_handler(SQLAlchemyError)
    async def database__error(request: Request, exc:SQLAlchemyError):
        print("SQLAlchemyError________________________________________________________________\n", exc)
        
        # print(str(exc))
        message = exc.args[0] if exc.args else "something went wrong"
        if "DETAIL:" in message:
            # Use regular expression to capture the text after 'DETAIL:' and remove unnecessary parts
            match = re.search(r"DETAIL: (.*)", message)
            if match:
                message = match.group(1).strip()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
            "is_success": False,
            "error": {
                    "message": message,
                    "resolution": "No resolution provided5",
                    # "stack": str(exc)
                }
            }
        )

       # # Handling ResponseValidationError
    @app.exception_handler(ResponseValidationError)
    async def response_validation_error(request: Request, exc:ResponseValidationError):
        print("ResponseValidationError________________________________________________________________\n")
        
        # print(str(exc))
        # message = exc.args[0] if exc.args else "something went wrong"
        # if "DETAIL:" in message:
        #     # Use regular expression to capture the text after 'DETAIL:' and remove unnecessary parts
        #     match = re.search(r"DETAIL: (.*)", message)
        #     if match:
        #         message = match.group(1).strip()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
            "is_success": False,
            "error": {
                    "message": "ResponseValidationError",
                    "resolution": "No resolution provided 01",
                    # "stack": str(exc)
                }
            }
        )

    # Handling Remaining All Error
    @app.exception_handler(422)
    async def internal_server_error(request, exc):
        print("Remaining All Error for 422________________________________________________________________\n", exc)
        return JSONResponse(
            content={
            "is_success": False,
            "error": {
                    "message": "Try to make defination of this error1",
                    "resolution":  "No resolution provided",
                }
            },
            status_code= 404,
        )
        
    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        print("Remaining All Error for 500________________________________________________________________\n", exc)
        return JSONResponse(
            content={
            "is_success": False,
            "error": {
                    "message": "Try to make defination of this error2",
                    "resolution":  "No resolution provided",
                }
            },
            status_code= 404,
        )

