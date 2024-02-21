import logging
from datetime import datetime
from fastapi import status, HTTPException
from app.data.access_permissions import USER_SCOPES, ADMIN_SCOPES


class ErrorHandler:
    @staticmethod
    def not_found(item: str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item} Not Found"
        )

    @staticmethod
    def user_unauthorized(message: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )

    @staticmethod
    def access_denied(item: str):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not have access to this {item}"
        )

    @staticmethod
    def bad_request(custom_message):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=custom_message)

    @staticmethod
    def too_many_request():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many request")

    @staticmethod
    def internal_server_error(error):
        logging.error(f"An error occurred at {datetime.now()}: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
