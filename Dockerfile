FROM python:3.12

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/app.sh

# docker build . -t fastapi_app:latest
# docker run -d -p 8000:8000 fastapi_app
# docker logs 8e69486aa4fccf1ad1298f63a1fe9c05e1d651c205fe1b6f4dd86dcd8cbe7fef