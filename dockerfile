FROM python:3.10

WORKDIR /blockchain

COPY ./requirements.txt /blockchain/requirements.txt

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /blockchain/requirements.txt

#   Copy all files from the project directory
COPY . /blockchain

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]