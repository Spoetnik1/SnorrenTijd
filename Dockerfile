# set base image (host OS)
FROM python:3.8-slim

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# check which ones are required, maybe all for openCV
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app

ENTRYPOINT ["tail", "-f", "/dev/null" ]

CMD ["RUN start.sh something something" ]
