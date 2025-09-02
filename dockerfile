FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV PORT=8080

# Command to run the app using Gunicorn
# Replace 'backend.app:app' with your Flask app path if different
CMD ["gunicorn", "-b", "0.0.0.0:8080", "backend.app:app"]
