FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV STATIC_PATH /app/bookMarkLibrary/static
FLASK_APP=bookMarkLibrary/run.py flask db upgrade