from app import app, entries


def test_non_ascii_wrong_password_does_not_crash(anonymous_client):
    response = anonymous_client.post("/login", data={"password": "falsch-ä"})
    assert response.status_code == 200


def test_login_without_configured_password_is_rejected(anonymous_client):
    app.config["PASSWORD"] = None
    assert anonymous_client.post("/login", data={}).status_code == 200
    with anonymous_client.session_transaction() as session:
        assert not session.get("logged_in", False)


def test_cross_origin_post_is_rejected(client):
    response = client.post(
        "/add_entry",
        data={"content": "Fremde Seite"},
        headers={"Origin": "https://example.invalid"},
    )
    assert response.status_code == 403
    assert entries == []


def test_same_origin_post_is_accepted(client):
    response = client.post(
        "/add_entry",
        data={"content": "Eigene Seite"},
        headers={"Origin": "http://localhost"},
    )
    assert response.status_code == 302
