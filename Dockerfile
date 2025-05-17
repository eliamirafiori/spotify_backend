FROM python:3.13-alpine

# create app directory into the container host
# RUN mkdir -p /usr/src/app

# change working dir of the project to "/spotify_clone"
WORKDIR /spotify_clone

# copy the "requirements.txt" file from the local dir to the working dir
COPY requirements.txt .

# run the python installation command for packages
RUN pip install --no-cache-dir -r requirements.txt

# copy all the files from the local dir to the working dir
COPY . .

# expose the port 8000
EXPOSE 8000

# create env variables
ENV DEBUG=False

# create a volume
# map the container volume "/spotify_clone" to the current host volume
# 
# VOLUME . /spotify_clone

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "./app/main.py"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

