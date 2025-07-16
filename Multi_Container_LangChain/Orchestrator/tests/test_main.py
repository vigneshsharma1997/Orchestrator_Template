from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"healthy"}
    

def test_process_query():
    response = client.get("/process",json = {"query":"What is LangChain"})
    assert response.status_code == 200
    assert "result" in response.json()
    assert "service" in response.json()
