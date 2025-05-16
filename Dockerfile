FROM python:3.13-alpine

# create app directory into the container host
RUN mkdir -p /usr/src/app

# change working dir of the project to /usr/src/app
WORKDIR /usr/src/app

# create a volume
# map the container volume "/usr/src/app" to the current host volume
# 
VOLUME . /usr/src/app

# copy the "requirements.txt" file from the host to the working dir
COPY requirements.txt .

# run the python installation command for packages
RUN pip install --no-cache-dir -r requirements.txt

# copy all the files from the host to the working dir
COPY . .

# expose the port 8000
EXPOSE 8000

# create env variables
ENV DEBUB=False

# CMD ["fastapi", "dev", "--workers", "4", "./app/main.py"]
CMD ["fastapi", "dev", "./app/main.py"]
