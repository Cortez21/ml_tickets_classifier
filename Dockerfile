FROM python:3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3.8", "-u", "server.py"]