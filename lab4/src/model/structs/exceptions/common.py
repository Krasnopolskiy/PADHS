from http import HTTPStatus

from model.structs.exceptions.base import BaseApiException


class InternalServerException(BaseApiException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    detail = "Something went wrong"


class ResourceNotFoundException(BaseApiException):
    status_code = HTTPStatus.NOT_FOUND
    detail = "Resource not found"
