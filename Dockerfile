FROM python:3.10-alpine

WORKDIR /opt/app

RUN apk add --no-cache ffmpeg

COPY requirements.txt /opt/app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "bot.py" ]