# Use an official Python image as base
FROM python:3.13.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Port (optional, for documentation)
EXPOSE 8000

# Default command (overridable in docker-compose or CLI)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
