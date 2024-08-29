from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_421_MISDIRECTED_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from app.config.logging_config import get_logger
from app.exceptions.exception import NoDataFoundException, RestClientException, UnauthorizedException, \
    ForbiddenException

logger = get_logger(class_name=__name__)


def add_exception_handler(app: FastAPI):
    @app.exception_handler(UnauthorizedException)
    async def handle_unauthorized_exception(request: Request, exc: UnauthorizedException):
        logger.error(exc.message)
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={'success': False,
                                                                        'message': exc.message,
                                                                        'status_code': exc.status})

    @app.exception_handler(ForbiddenException)
    async def handle_forbidden_exception(request: Request, exc: ForbiddenException):
        logger.error(exc.message)
        return JSONResponse(status_code=HTTP_403_FORBIDDEN, content={'success': False,
                                                                     'message': exc.message,
                                                                     'status_code': exc.status})

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        logger.exception(exc)
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={'success': False,
                                                                       'message': str(exc)})

    @app.exception_handler(RestClientException)
    async def handle_no_data_found_exception(request: Request, exc: RestClientException):
        logger.error(exc.message)
        return JSONResponse(status_code=HTTP_421_MISDIRECTED_REQUEST, content={'success': False,
                                                                               'message': exc.message,
                                                                               'status_code': exc.status})

    @app.exception_handler(NoDataFoundException)
    async def handle_no_data_found_exception(request: Request, exc: NoDataFoundException):
        logger.error(exc.message)
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={'success': False,
                                                                       'message': exc.message,
                                                                       'status_code': exc.status})
