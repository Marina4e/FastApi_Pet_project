def get_token(client, email, password):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })

    assert res.status_code == 200, res.json()  # 👈 ВАЖНО

    return res.json()["access_token"]


def test_get_books(client, user_test):
    token = get_token(client, user_test.email, "123456")

    res = client.get("/books/", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200


def test_create_book_admin(client, admin_test):
    token = get_token(client, admin_test.email, "123456")
    res = client.post("/books/", params={
        "title": "Test",
        "author": "Me",
        "year": 2024
    }, headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200


def test_create_book_user_forbidden(client, user_test):
    token = get_token(client, user_test.email, "123456")
    res = client.post("/books/", params={
        "title": "Test",
        "author": "Me",
        "year": 2024
    }, headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 403
