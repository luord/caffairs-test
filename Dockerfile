FROM luord/docker

ADD ./ ./

RUN poetry install

CMD uvicorn eye.asgi:application --host 0.0.0.0 --port 8000
