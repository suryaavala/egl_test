FROM python:3.9.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY models/ /app/models/
COPY Pipfile* /app/
COPY setup.* /app/
COPY *.ini /app/

RUN pip3 install pipenv==2022.1.8 &&\
    pipenv install --system --deploy


COPY linear_regressor/ /app/linear_regressor/
COPY main.py /app/main.py


# $PORT is set by google cloud run
CMD exec python3 main.py serve --host="0.0.0.0" --port=$PORT --with-gunicorn
