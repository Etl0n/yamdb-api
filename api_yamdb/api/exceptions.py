from rest_framework import status
from rest_framework.exceptions import APIException


class ExistRewies(APIException):
    """Исключение для API, когда не найден отзыв в БД."""

    status_code = status.HTTP_400_BAD_REQUEST


class TitleNotExist(APIException):
    """Исключение для API, когда не найден произведение в БД."""

    status_code = status.HTTP_404_NOT_FOUND
