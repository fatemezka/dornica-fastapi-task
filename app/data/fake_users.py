from datetime import datetime, timezone
from app.utils.password_operator import get_password_hash

FAKE_USERS = [
    {
        "userName": "amir",
        "fullName": "Amir Amiri",
        "email": "amir@gmail.com",
        "hashedPassword": get_password_hash("1234@Amir"),
        "gender": "male",
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    },
    {
        "userName": "sahar",
        "fullName": "Sahar Mahdavi",
        "email": "sahar@gmail.com",
        "hashedPassword": get_password_hash("1234@Sahar"),
        "gender": "female",
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    },
    {
        "userName": "homayun",
        "fullName": "Homayun Musavi",
        "email": "homayun@gmail.com",
        "hashedPassword": get_password_hash("1234@Homayun"),
        "gender": "male",
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    }
]
