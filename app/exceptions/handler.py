from fastapi.responses import JSONResponse
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from exceptions.models import CustomError, ExceptionContent

def register_all_errors(app: FastAPI):
    # Handling CustomError 
    @app.exception_handler(CustomError)
    async def database__error(request, exc):
        # print(str(exc))
        return JSONResponse(
            content={
            "is_success": False,
            "error": {
                    "message": exc.message,
                    "resolution": exc.resolution or "No resolution provided",
                }
            },
            status_code=exc.status_code,
        )
    # # Handling SQLAlchemyError
    # @app.exception_handler(SQLAlchemyError)
    # async def database__error(request, exc):
    #     print("SQLAlchemyError________________________________________________________________")
    #     # print(str(exc))
    #     return JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content={
    #         "is_success": False,
    #         "error": {
    #                 "message": exc.message,
    #                 "resolution": exc.resolution or "No resolution provided",
    #             }
    #         }
    #     )
    #     # Handling Remaining All Error
    # @app.exception_handler(500)
    # async def internal_server_error(request, exc):
    #     # print("Remaining All Error________________________________________________________________")
    #     return JSONResponse(
    #         content={
    #         "is_success": False,
    #         "error": {
    #                 "message": "exc.message",
    #                 "resolution":  "No resolution provided",
    #             }
    #         },
    #         status_code= 404,
    #     )

