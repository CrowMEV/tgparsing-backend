from fastapi import status

# from fastapi_users.router.common import ErrorModel, ErrorCode


# HTTP_400 = {
#     status.HTTP_400_BAD_REQUEST: {
#         "model": ErrorModel,
#         "content": {
#             "application/json": {
#                 "examples": {
#                     ErrorCode.LOGIN_BAD_CREDENTIALS: {
#                         "summary": "Bad credentials or "
#                         "the user is inactive.",
#                         "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
#                     },
#                     ErrorCode.LOGIN_USER_NOT_VERIFIED: {
#                         "summary": "The user is not verified.",
#                         "value": {
#                             "detail": ErrorCode.LOGIN_USER_NOT_VERIFIED
#                         },
#                     },
#                 }
#             }
#         },
#     },
# }

HTTP_401 = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    }
}

HTTP_403 = {
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser or an admin.",
    }
}

HTTP_404 = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Missing token or inactive user.",
    }
}

HTTP_201 = {
    201: {"content": {"application/json": {"example": {"detail": "created"}}}}
}
