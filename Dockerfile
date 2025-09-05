FROM python:3-alpine AS builder

COPY . /app
WORKDIR /app
 
RUN python3 -m venv venv
RUN apk add --no-cache build-base
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
COPY requirements.txt .
RUN pip install -r requirements.txt
 
# Stage 2
FROM python:3-alpine AS runner
 
WORKDIR /app
 
COPY --from=builder /app/venv venv
COPY . .
 
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app
 
EXPOSE 8080
 
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "app:app"]