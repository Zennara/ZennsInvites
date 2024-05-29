# Use the official Python base image
FROM python:3.11.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Specify the command to run the bot
CMD ["python", "main.py"]
