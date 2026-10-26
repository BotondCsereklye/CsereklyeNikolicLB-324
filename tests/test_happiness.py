from app import entries


def test_happiness_is_displayed(client):
    client.post("/add_entry", data={"content": "Ein guter Tag", "happiness": "😃"})
    response = client.get("/")
    assert '<span aria-label="Stimmung">😃</span>' in response.get_data(as_text=True)
    assert "Ein guter Tag" in response.get_data(as_text=True)


def test_existing_calls_get_neutral_mood(client):
    client.post("/add_entry", data={"content": "Bestehender Aufruf"})
    assert entries[0].happiness == "😐"


def test_invalid_happiness_is_rejected(client):
    response = client.post(
        "/add_entry", data={"content": "Test", "happiness": "<script>"}
    )
    assert response.status_code == 400
    assert entries == []
