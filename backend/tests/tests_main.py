from fastapi.testclient import TestClient
from app.main import app  # Absolute import
client = TestClient(app)

def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI WebSocket Server is running!"}