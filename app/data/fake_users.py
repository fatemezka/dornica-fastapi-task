from datetime import datetime, timezone
from app.utils.password_operator import get_password_hash
from app.models import Gender

FAKE_USERS = [
    {
        "userName": "amir",
        "fullName": "Amir Amiri",
        "email": "amir@gmail.com",
        "hashedPassword": get_password_hash("1234@Amir"),
        "gender":  Gender.MALE,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "userName": "sahar",
        "fullName": "Sahar Mahdavi",
        "email": "sahar@gmail.com",
        "hashedPassword": get_password_hash("1234@Sahar"),
        "gender":  Gender.FEMALE,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "userName": "homayun",
        "fullName": "Homayun Musavi",
        "email": "homayun@gmail.com",
        "hashedPassword": get_password_hash("1234@Homayun"),
        "gender":  Gender.MALE,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
]
