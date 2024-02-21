from fastapi import Request, Response
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import redis_client
from datetime import datetime
from app.utils.error_handler import ErrorHandler
from app.authentication import token_encoder
from app.utils.redis_operator import get_redis_value, increase_redis_request_ip
from app.models import User
from app.database import SessionLocal
from sqlalchemy import select


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # check ip
        self.check_allowed_ip(request)

        # check request count per minute
        if request.method == "POST" and request.url.path == "/user/token":
            self.check_request_attempts(request)

        # validate token from redis
        await self.validate_token(request)

        # log request
        self.log_request(request)

        # Continue processing the request
        response: Response = await call_next(request)

        # if failed
        if (response.status_code != 200):
            print(
                f"Your request failed with status code {response.status_code}")

        return response

    def log_request(self, request: Request):
        if request.client:
            client_ip = request.client.host
        else:
            client_ip = "N/A"  # for unit-testing

        current_date = str(datetime.now())
        request_data = f"Date: {current_date}, Request Method: {request.method}, Client Ip: {client_ip} {request.headers}\n"
        with open("request_logger.log", 'a') as log_file:
            log_file.write(request_data)

    def check_allowed_ip(self, request: Request):
        allowed_ip_list = redis_client.lrange("allowed_ip_list", 0, -1) or []

        if request.client:
            client_ip = request.client.host
        else:
            client_ip = "N/A"  # for unit-testing

        if client_ip != "N/A" and client_ip not in allowed_ip_list:
            raise ErrorHandler.access_denied(
                "url (based on your blocked IP) - check allowed IPs")  # TODO fix raise error

    async def validate_token(self, request: Request):
        if "auth-token" not in request.headers:
            return

        bearer, token = request.headers["auth-token"].split(" ")
        encoded_token = token_encoder(token=token)
        user_id = encoded_token["user_id"]
        db = SessionLocal()

        current_user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

        existing_redis_token = get_redis_value(key=current_user.email)
        if not existing_redis_token:
            raise ErrorHandler.user_unauthorized(
                message="Your token is expired. Please try to login again.")  # TODO fix raise error

    def check_request_attempts(self, request: Request):
        if not request.client:
            return
        client_ip = request.client.host
        increase_redis_request_ip(client_ip)  # TODO fix raise error
