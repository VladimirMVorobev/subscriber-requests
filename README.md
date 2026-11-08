# Subscriber Requests API

Сервис для сбора и сохранения обращений абонентов.

## Технологии
- Python
- FastAPI
- Pydantic
- Pytest

## Установка

```bash
python -m pip install fastapi 'uvicorn[standard]' pydantic[email] pytest httpx
```

## Запуск

```bash
python -m uvicorn app.main:app --reload
```

Документация API: http://127.0.0.1:8000/docs

## Возможности
- Проверка данных абонента
- Создание обращений через POST /requests
- Сохранение обращений в requests.json
- Автоматические тесты

## Тестирование

```bash
python -m pytest -v
```
