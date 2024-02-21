from app.database import redis_client
import os
from app.utils.error_handler import ErrorHandler

from dotenv import load_dotenv
load_dotenv()


def increase_redis_request_ip(ip):
    existing_redis_ip = get_redis_value(ip)
    if not existing_redis_ip:
        redis_client.setex(name=ip, time=60, value=1)
        return
    counter = int(redis_client.get(name=ip))
    if counter >= 5:
        raise ErrorHandler.too_many_request()

    counter += 1
    remaining_ttl = redis_client.ttl(ip)
    redis_client.setex(name=ip, time=remaining_ttl, value=counter)


def store_redis_token(user, token):
    redis_key = user.email
    redis_value = token

    # set to redis
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    redis_client.setex(
        name=redis_key,
        time=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        value=redis_value)


def remove_redis_token(user):
    redis_key = user.email
    check_redis_key = redis_client.get(name=redis_key)
    if check_redis_key:
        redis_client.delete(redis_key)


def get_redis_value(key):
    check_redis_key = redis_client.get(name=key)
    return bool(check_redis_key)
