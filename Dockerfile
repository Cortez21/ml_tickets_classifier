FROM python:3.8

RUN mkdir -p /urs/src/app
WORKDIR /urs/src/app

COPY . /urs/src/app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python3.8", "-u", "server.py"]