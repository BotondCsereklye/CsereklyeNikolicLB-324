from app import entries


def test_add_entry(client):
    # Test adding an entry
    response = client.post("/add_entry", data={"content": "Test Entry Content"})

    # Check if the response is a redirect to the index page
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    # Check if the entry was added to the database
    entry = entries[0]
    assert entry is not None
    assert entry.content == "Test Entry Content"
