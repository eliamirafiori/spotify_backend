FROM python:3.13-alpine

# create app directory into the container host
# RUN mkdir -p /usr/src/app

# change working dir of the project to "/spotify_clone"
WORKDIR /spotify_clone

# copy the "requirements.txt" file from the host to the working dir
COPY requirements.txt .

# run the python installation command for packages
RUN pip install --no-cache-dir -r requirements.txt

# copy all the files from the host to the working dir
COPY . .

# expose the port 8000
EXPOSE 80

# create env variables
ENV DEBUB=False

# create a volume
# map the container volume "/spotify_clone" to the current host volume
# 
# VOLUME . /spotify_clone

# CMD ["fastapi", "dev", "--workers", "4", "./app/main.py"]
CMD ["fastapi", "dev", "./app/main.py"]
# CMD ["uvicorn", "./app/main:app", "--host", "0.0.0.0", "--port", "80"]
