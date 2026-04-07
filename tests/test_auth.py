import uuid
from app.settings import settings
print("DB:", settings.DATABASE_URL)


def test_register(client):
    email = f"new_{uuid.uuid4()}@test.com"

    response = client.post("/register", json={
        "email": email,
        "password": "123456",
        "role": "user"
    })
    assert response.status_code == 200


def test_login(client, admin_test):
    response = client.post(
        "/login",
        data={"username": admin_test.email,
              "password": "123456"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
