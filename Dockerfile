FROM python:3.9.19-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /flask-app

RUN pip --version

COPY requirements.txt requirements.txt
RUN cat requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pytest

RUN flask db init
RUN flask db migrate -m "Initial migration."
RUN flask db upgrade

EXPOSE 8000

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=localhost", "port=8000", "--debug"]
