# Text file contains instructions needed to build the Docker Image.
FROM python:3.7

LABEL maintainer="Automation"
#ENV PROJ=""
#ENV RELEASE=""
#ENV TESTSET=""
#ENV GRIDURL =""

# copy the dependencies file to the working directory
COPY ./requirements.txt /requirements.txt
# install dependencies
RUN pip install -r /requirements.txt

# set the working directory in the container
RUN mkdir /workspace
WORKDIR /workspace

# copy the content of the local  directory to the working directory
COPY    . .

# command to run on container start


CMD ["python", "runAll.py" ]

