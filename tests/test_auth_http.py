from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_requires_api_key():
    r = client.post("/chat/", json={"message": "hola"})
    assert r.status_code in (403, 401)
