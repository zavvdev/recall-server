from rest_framework import status
from rest_framework.exceptions import APIException

from shared.messages import Messages


class AppException(APIException):
    def __init__(
        self,
        message=Messages.UNEXPECTED_ERROR,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        data=None,
    ):
        self.status_code = status_code
        self.message = message
        self.data = data
        super().__init__(detail=message)
