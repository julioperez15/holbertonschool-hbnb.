# Use an base image of Alpine Linux with Python 3.9
FROM python:3.9-alpine

# Stablish the working directory in the /app
WORKDIR /app

# Copy the file "requirements.txt" in the working directory 
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the file app in the working directory
COPY . .

# Stablish an enviroment variable to the port 8000 as default port to run the app
ENV PORT 8000

# Define a volume to the persistent data
VOLUME /app/data

# Expose the configured port
EXPOSE $PORT

# Define the command to execute Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]