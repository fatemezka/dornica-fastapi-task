# from app.utils.error_handler import ErrorHandler
# import os
# from app.database import create_redis_pool


# async def increase_redis_request_ip(ip):
#     redis_pool = await create_redis_pool()
#     existing_redis_ip = await get_redis_value(ip)
#     if not existing_redis_ip:
#         await redis_pool.setex(name=ip, time=60, value=1)
#         return
#     counter = int(await redis_pool.get(name=ip))
#     if counter >= 5:
#         raise ErrorHandler.too_many_request()

#     counter += 1
#     remaining_ttl = await redis_pool.ttl(ip)
#     await redis_pool.setex(name=ip, time=remaining_ttl, value=counter)


# async def store_redis_token(user, token):
#     redis_pool = await create_redis_pool()
#     redis_key = user.email
#     redis_value = token

#     # set to redis
#     ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
#     await redis_pool.setex(
#         name=redis_key,
#         time=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#         value=redis_value)


# async def remove_redis_token(user):
#     redis_pool = await create_redis_pool()
#     redis_key = user.email
#     check_redis_key = await redis_pool.get(name=redis_key)
#     if check_redis_key:
#         await redis_pool.delete(redis_key)


# async def get_redis_value(key):
#     redis_pool = await create_redis_pool()
#     check_redis_key = await redis_pool.get(name=key)
#     return bool(check_redis_key)
