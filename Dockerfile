FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv pip install fastapi uvicorn

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", $PORT]
