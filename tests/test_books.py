def create_book(client, token, title="Test", author="Me", year=2024):
    return client.post(
        "/books/",
        json={
            "title": title,
            "author": author,
            "year": year
        },
        headers={"Authorization": f"Bearer {token}"}
    )


def test_get_books(client, user_test, get_token):
    token = get_token(user_test.email, "123456")

    res = client.get("/books/", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200


def test_get_one_book(client, admin_test, get_token):
    token = get_token(admin_test.email, "123456")

    res = create_book(client, token)
    book_id = res.json()["id"]

    res = client.get(f"/books/{book_id}", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200
    data = res.json()

    assert data["id"] == book_id


def test_create_book_admin(client, admin_test, get_token):
    token = get_token(admin_test.email, "123456")

    res = create_book(client, token)

    assert res.status_code == 200


def test_create_book_user_forbidden(client, user_test, get_token):
    token = get_token(user_test.email, "123456")

    res = create_book(client, token)

    assert res.status_code == 403


def test_update_book_admin(client, admin_test, get_token):
    token = get_token(admin_test.email, "123456")

    res = create_book(client, token)
    book_id = res.json()["id"]

    res = client.put(
        f"/books/{book_id}",
        json={
            "title": "New",
            "author": "B",
            "year": 2024
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json()["title"] == "New"


def test_delete_book_admin(client, admin_test, get_token):
    token = get_token(admin_test.email, "123456")

    res = create_book(client, token)
    book_id = res.json()["id"]

    res = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200


def test_get_one_book_not_found(client, get_token, user_test):
    token = get_token(user_test.email, "123456")

    res = client.get(
        "/books/9999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 404
