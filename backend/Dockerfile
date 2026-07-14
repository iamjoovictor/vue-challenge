FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Ensure the logs directory exists
RUN mkdir -p logs

EXPOSE 8000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
