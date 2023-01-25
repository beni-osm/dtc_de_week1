FROM python:3.8

WORKDIR /data_ingestion

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ingestion_script.py ingestion_script.py
COPY .env .env

CMD [ "python", "ingestion_script.py"]
