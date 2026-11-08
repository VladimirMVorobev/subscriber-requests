
from fastapi import FastAPI

from app.models import SubscriberRequest
from app.storage import save_request


app = FastAPI(
    title="Subscriber Requests API",
    description="Сервис для сбора обращений абонентов",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Сервис работает!"}


@app.post("/requests", status_code=201)
def create_request(request: SubscriberRequest):
    saved_request = save_request(request)

    return {
        "message": "Обращение успешно сохранено",
        "data": saved_request,
    }
