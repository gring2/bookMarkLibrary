FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV STATIC_PATH /app/bookMarkLibrary/static
ENV GCSFUSE_REPO gcsfuse-stretch
RUN echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list
RUN curl http://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update -y
RUN apt-get install gcsfuse -y

RUN echo "user_allow_other" >> /etc/fuse.conf

