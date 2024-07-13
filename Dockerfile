FROM python:3.9.19-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /common

RUN pip --version

COPY . . 

ENV FLASK_APP=app.py

COPY requirements.txt requirements.txt
RUN cat requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pytest
RUN pip install gunicorn

#RUN flask db init
#RUN flask db migrate -m "Initial migration."

#RUN chmod +x entrypoint.sh

#ENTRYPOINT ["/common/entrypoint.sh"]

EXPOSE 8000

#COPY . .

#RUN flask db upgrade

#CMD [ "python3", "-m" , "flask", "run", "--host=localhost", "port=8000", "--debug"]
#CMD [ "python3", "-m", "flask", "db", "upgrade"]

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]

#RUN chmod +x entrypoint.sh

#ENTRYPOINT ["/common/entrypoint.sh"]
