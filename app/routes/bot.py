from fastapi import APIRouter
from app.utils.weatherapi_receiver import main
from app.database import redis_client

router = APIRouter()


# create time.csv file
@router.get("/")
async def create_time_route():
    # main() # TODO fix
    return {"message": "3 Months weather info saved in 'time.csv' file."}