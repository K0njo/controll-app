#FROM python:3.8.1
#
#EXPOSE 8000
#WORKDIR /app
#
#COPY requirement.txt requirements.txt
#
#RUN pip install -r requirements.txt
#
#COPY . ./
#
#CMD uvicorn --host=0.0.0.0 src.main:app

# Use an official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirement.txt

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]