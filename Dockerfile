# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install required dependencies directly
RUN pip install --no-cache-dir Flask gunicorn Flask-SQLAlchemy psycopg2-binary matplotlib pandas circlify reportlab

# Expose port 5000 for Flask
EXPOSE 5000

# Define the command to run the application
CMD ["python", "run.py"]
