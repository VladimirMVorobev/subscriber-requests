
import json
from pathlib import Path
from uuid import uuid4

from app.models import SubscriberRequest


DATA_FILE = Path(__file__).resolve().parent.parent / "requests.json"


def save_request(request: SubscriberRequest) -> dict:
    record = {
        "id": str(uuid4()),
        **request.model_dump(mode="json"),
    }

    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)
    else:
        records = []

    records.append(record)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

    return record
