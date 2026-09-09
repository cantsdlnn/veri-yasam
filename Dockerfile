FROM python:3.11-slim

WORKDIR /app
RUN groupadd --system veriyasam && useradd --system --gid veriyasam veriyasam
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN mkdir -p /app/var && chown -R veriyasam:veriyasam /app

USER veriyasam

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
