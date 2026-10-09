import pytest

from app import app, entries


@pytest.fixture(autouse=True)
def isolated_entries():
    entries.clear()
    yield
    entries.clear()


@pytest.fixture()
def client():
    app.config.update(TESTING=True, PASSWORD="test-password", SECRET_KEY="test-key")
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["logged_in"] = True
        yield client


@pytest.fixture()
def anonymous_client():
    app.config.update(TESTING=True, PASSWORD="test-password", SECRET_KEY="test-key")
    with app.test_client() as client:
        yield client
