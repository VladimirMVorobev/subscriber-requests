import json

from app import storage


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Сервис работает!"
    }


def test_invalid_phone():
    request_data = {
        "last_name": "Иванов",
        "first_name": "Иван",
        "birth_date": "2000-05-15",
        "phone": "12345",
        "email": "ivan@example.com",
        "reasons": ["нет доступа к сети"],
        "problem_datetime": "2025-01-15T10:30:00+03:00",
    }

    response = client.post("/requests", json=request_data)

    assert response.status_code == 422



def test_create_request(tmp_path, monkeypatch):
    test_file = tmp_path / "requests.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    request_data = {
        "last_name": "Иванов",
        "first_name": "Иван",
        "birth_date": "2000-05-15",
        "phone": "+79991234567",
        "email": "ivan@example.com",
        "reasons": ["нет доступа к сети"],
        "problem_datetime": "2025-01-15T10:30:00+03:00",
    }

    response = client.post("/requests", json=request_data)

    assert response.status_code == 201
    assert response.json()["message"] == "Обращение успешно сохранено"

    assert test_file.exists()

    with test_file.open("r", encoding="utf-8") as file:
        saved_requests = json.load(file)

    assert len(saved_requests) == 1
    assert saved_requests[0]["last_name"] == "Иванов"
    assert saved_requests[0]["phone"] == "+79991234567"
    assert "id" in saved_requests[0]
