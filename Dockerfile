# Dockerfile for a Python application
FROM python:3.11-slim

WORKDIR /app

# Install Flask in one RUN
RUN pip install --no-cache-dir flask

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8496
CMD ["python", "app.p"]