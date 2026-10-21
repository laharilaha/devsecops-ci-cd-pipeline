import pytest
from app.main import create_app

@pytest.fixture()
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["project"] == "DevSecOps CI/CD Pipeline"

def test_list_items_initially_empty(client):
    response = client.get("/api/items")
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_and_list_item(client):
    created = client.post("/api/items", json={"name": "demo"})
    assert created.status_code == 201
    assert created.get_json()["name"] == "demo"
    assert client.get("/api/items").get_json()[0]["name"] == "demo"

@pytest.mark.parametrize("payload", [{}, {"name": ""}, {"name": "   "}, {"name": 123}])
def test_invalid_item_name_returns_400(client, payload):
    assert client.post("/api/items", json=payload).status_code == 400

def test_search_items(client):
    client.post("/api/items", json={"name": "secure pipeline"})
    response = client.get("/api/items/search?q=secure")
    assert response.status_code == 200
    assert response.get_json()[0]["name"] == "secure pipeline"

def test_security_headers_are_set(client):
    response = client.get("/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Cache-Control"] == "no-store"
