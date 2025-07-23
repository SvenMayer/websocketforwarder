FROM python:3.10-slim

# Avoid Python buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose the WebSocket port
EXPOSE 10000

CMD ["python3", "app.py"]
