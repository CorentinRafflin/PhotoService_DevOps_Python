# Use an official Python runtime as a parent image
FROM python:3-slim

# copy only the requirements.txt file at first
COPY requirements.txt /photo_service/

# Set the working directory to /app
WORKDIR /photo_service

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
ADD . /photo_service

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python3", "photo_service_main.py"]
