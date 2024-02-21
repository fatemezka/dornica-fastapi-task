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
        "userName": "sara",
        "fullName": "Sara Mahdavi",
        "email": "sara@gmail.com",
        "hashedPassword": get_password_hash("1234@Sara"),
        "gender": "female",
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    },
    {
        "userName": "hana",
        "fullName": "Hana Musavi",
        "email": "hana@gmail.com",
        "hashedPassword": get_password_hash("1234@Hana"),
        "gender": "female",
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    }
]
