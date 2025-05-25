# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# First, create a requirements.txt if you haven't already:
# pip freeze > requirements.txt
RUN pip install --no-cache-dir Flask requests

# Expose port 8000 (where the Flask app will run)
EXPOSE 8000

# Run the Flask application
# Use 0.0.0.0 to make the server accessible from outside the container
CMD ["python", "app.py"]