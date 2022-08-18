FROM python:3.10

WORKDIR /blockchain_docker
COPY ./requirements.txt /blockchain_docker/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /blockchain_docker/requirements.txt

#   Copy all files from the project directory
COPY . /blockchain

EXPOSE 8080
CMD ["./run.sh"]
