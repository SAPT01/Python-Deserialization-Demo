FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=development
EXPOSE 5000

CMD ["python", "app.py"]
