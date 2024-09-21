# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container at /app
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH /usr/src/app

# Ensure the log directory exists
RUN mkdir -p logs

# Command to run on container start
CMD ["python", "src/main.py"]
