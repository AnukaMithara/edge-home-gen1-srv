from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.exceptions.no_data_found_exception import NoDataFoundException


def add_exception_handler(app: FastAPI):
    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        return JSONResponse(status_code=400, content=str(exc))

    @app.exception_handler(NoDataFoundException)
    async def handle_no_data_found_exception(request: Request, exc: NoDataFoundException):
        return JSONResponse(status_code=404, content=exc.to_dict())
