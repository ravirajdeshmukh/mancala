FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Set default command
CMD ["python", "main.py"]
