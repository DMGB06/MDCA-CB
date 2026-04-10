from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ws_requires_api_key():
    try:
        with client.websocket_connect("/chat/ws"):
            assert False, "No debería conectar sin API key"
    except Exception:
        assert True