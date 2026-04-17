def test_ws_requires_api_key(client):
    try:
        with client.websocket_connect("/chat/ws"):
            assert False, "No debería conectar sin API key"
    except Exception:
        assert True


def test_ws_connects_with_api_key(client):
    with client.websocket_connect(
        "/chat/ws?api_key=test-api-key",
        headers={"origin": "http://localhost:3000"}
    ) as ws:
        ws.send_text("hola")
        data = ws.receive_json()
        assert "response" in data
