# Dockerfile that includes the app.py and python 3.10.11
FROM python:3.10.11-alpine as ai-text-game
COPY ./src /app/src
COPY ./requirements.txt /app
COPY ./config /app/config
COPY ./app.py /app
COPY ./.env /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]