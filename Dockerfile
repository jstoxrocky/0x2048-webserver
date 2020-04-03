FROM python:3.7-alpine
WORKDIR /webserver
ENV FLASK_APP webserver/application.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV=production
RUN apk update && apk upgrade && \
    apk add --no-cache gcc musl-dev linux-headers git bash yarn
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY setup.py setup.py
RUN python setup.py install
COPY . .
RUN yarn install
RUN yarn global add parcel-bundler
RUN yarn tsc
RUN yarn bundle
CMD flask run --host 0.0.0.0 --port $PORT
