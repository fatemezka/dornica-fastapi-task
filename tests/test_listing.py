from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import drop_all_tables, create_all_tables, SessionLocal
from app.models import User, Listing
from datetime import datetime, timezone
from app.utils.password_operator import get_password_hash


client = TestClient(app)


test_user = {
    "id": 1,
    "userName": "fateme",
    "fullName": "Fateme",
    "email": "fateme@gmail.com",
    "hashedPassword": get_password_hash("1234@Fateme"),
    "dob": None,
    "gender": "female",
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
}
test_listing = {
    "id": 1,
    "type": "apartment",
    "availableNow": True,
    "ownerId": 1,  # id of user
    "address": "Tehran",
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
}


def initial_user_table():
    db = SessionLocal()
    new_user = User(
        id=test_user["id"],
        userName=test_user["userName"],
        fullName=test_user["fullName"],
        email=test_user["email"],
        hashedPassword=test_user["hashedPassword"],
        dob=test_user["dob"],
        gender=test_user["gender"],
        createdAt=test_user["createdAt"],
        updatedAt=test_user["updatedAt"]
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    db.close()


def initial_listing_table():
    db = SessionLocal()
    new_listing = Listing(
        id=test_listing["id"],
        type=test_listing["type"],
        availableNow=test_listing["availableNow"],
        ownerId=test_listing["ownerId"],
        address=test_listing["address"],
        createdAt=test_listing["createdAt"],
        updatedAt=test_listing["updatedAt"]
    )
    db.add(new_listing)
    await db.commit()
    await db.refresh(new_listing)
    db.close()


# Drop users and listings tables
drop_all_tables()
create_all_tables()

# add new user and listing
initial_user_table()
initial_listing_table()


def get_token():
    response = client.post(
        url="/user/token",
        json={
            "userName": test_user["userName"],
            "password": "1234@Fateme"
        })
    token_info = response.json()
    token = token_info["token"]
    return token


# 1. test get all
@pytest.mark.asyncio
def test_get_all_listings():
    token = get_token()

    response = client.get(
        url=f"/listing/all",
        headers={"auth-token": f"bearer {token}"})
    assert response.status_code == 200

    all_listings = response.json()
    assert len(all_listings) >= 1


# 2. test get by id
@pytest.mark.asyncio
def test_get_listing():
    token = get_token()
    listing_id = test_listing['id']
    get_listing_response = client.get(
        url=f"/listing/{listing_id}",
        headers={"auth-token":  f"bearer {token}"})
    assert get_listing_response.status_code == 200

    get_listing = get_listing_response.json()
    assert get_listing["type"] == "apartment"
    assert get_listing["address"] == "Tehran"


# 3. test create
@pytest.mark.asyncio
def test_create_listing():
    token = get_token()
    response = client.post(
        url="/listing/",
        json={
            "type": "house",
            "availableNow": False,
            "address": "Shiraz"
        },
        headers={"auth-token": f"bearer {token}"})
    assert response.status_code == 200

    new_listing = response.json()
    assert new_listing["availableNow"] == False
    assert new_listing["address"] == "Shiraz"


# 4. test update
@pytest.mark.asyncio
def test_update_listing():
    token = get_token()
    listing_id = test_listing['id']
    update_listing_response = client.put(
        url=f"/listing/{listing_id}",
        json={
            "type": test_listing["type"],
            "availableNow": test_listing["availableNow"],
            "address": "Kish"
        },
        headers={"auth-token":  f"bearer {token}"})
    assert update_listing_response.status_code == 200

    updated_message = update_listing_response.json()
    assert updated_message["message"] == "Listing updated successfully"


# 5. test delete
@pytest.mark.asyncio
def test_delete_listing():
    token = get_token()
    listing_id = test_listing['id']
    delete_listing_response = client.delete(
        url=f"/listing/{listing_id}",
        headers={"auth-token":  f"bearer {token}"})
    assert delete_listing_response.status_code == 200

    deleted_message = delete_listing_response.json()
    assert deleted_message["message"] == "Listing deleted successfully"
