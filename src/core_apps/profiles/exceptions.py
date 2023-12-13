from rest_framework.exceptions import APIException


class CantFollowYourself(APIException):
    """Exception for attempting to follow yourself"""

    status_code = 403
    default_detail = "You can't follow yourself."
    default_code = "forbidden"
