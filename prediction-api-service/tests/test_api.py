from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_invalid_features():
    response = client.post("/predict", json={
        "user_id": "u1",
        "features_for_prediction": [1.0]
    })
    assert response.status_code == 400
