FROM python:3-alpine

# Create app directory
RUN mkdir -p /usr/src/app

# Change working dir to /usr/src/app
WORKDIR /usr/src/app

VOLUME . /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE 8000

CMD ["fastapi", "dev", "--workers", "4", "./app/main.py"]
