from datetime import datetime

from app import Entry, entries


def test_login_page_and_wrong_password(anonymous_client):
    assert anonymous_client.get("/login").status_code == 200
    response = anonymous_client.post("/login", data={"password": "wrong"})
    assert response.status_code == 200
    with anonymous_client.session_transaction() as session:
        assert not session.get("logged_in", False)


def test_correct_password_and_logout(anonymous_client):
    response = anonymous_client.post("/login", data={"password": "test-password"})
    assert response.status_code == 302
    with anonymous_client.session_transaction() as session:
        assert session["logged_in"] is True
    assert anonymous_client.get("/logout").status_code == 302
    with anonymous_client.session_transaction() as session:
        assert "logged_in" not in session


def test_anonymous_user_cannot_add_or_read_entries(anonymous_client):
    entries.append(Entry(content="Private entry"))
    response = anonymous_client.post("/add_entry", data={"content": "Unwanted"})
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"
    assert len(entries) == 1
    assert b"Private entry" not in anonymous_client.get("/").data


def test_blank_and_too_long_entries_are_rejected(client):
    for content in ["", "   ", "a" * 5001]:
        assert client.post("/add_entry", data={"content": content}).status_code == 400
    assert entries == []


def test_entry_limit_and_timestamp(client):
    assert client.post("/add_entry", data={"content": "a" * 5000}).status_code == 302
    assert isinstance(entries[0].timestamp, datetime)


def test_content_is_escaped(client):
    client.post("/add_entry", data={"content": "<script>alert(1)</script>"})
    html = client.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_health_and_security_headers(anonymous_client):
    response = anonymous_client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
