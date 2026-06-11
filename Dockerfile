FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "mkdir -p /app/logs && touch /app/logs/app.log && python -c \"from todo_project import app, db; ctx = app.app_context(); ctx.push(); db.create_all(); ctx.pop()\" && flask --app run:app run --host=0.0.0.0 --port=5000"]
