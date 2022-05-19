# set base image (host OS)
FROM python:3.8-slim

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

ADD snorrenapp /app/snorrenapp

COPY . /app

ENTRYPOINT ["tail", "-f", "/dev/null" ]

# CMD ["snorrenapp/main.py" ]