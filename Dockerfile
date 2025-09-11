# Build stage 
FROM python:3.12-slim AS build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /app /app

EXPOSE 8888 8501

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
