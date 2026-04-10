from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_rejects_empty_message():
    r = client.post(
        "/chat/",
        headers={"X-API-Key": "test-api-key"},  # key válida
        json={"message": "   "}
    )
    assert r.status_code == 422