FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat for database checking
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Copy project
COPY . .

# Run migrations (only when running the container)
ENTRYPOINT ["python", "manage.py", "migrate"]

# Expose the port
EXPOSE 8000

# Start the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
