# 1. Use an official, lightweight Python image
FROM python:3.13-slim

# 2. Tell Python not to write annoying .pyc files and to print logs instantly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Create a folder inside the container called /app
WORKDIR /app

# 4. Copy your requirements file and install the packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your Django project into the container
COPY . /app/

# 6. Expose port 8000 so the outside world can talk to it
EXPOSE 8000

# 7. The command to start the server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]