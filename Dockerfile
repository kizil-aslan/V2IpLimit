FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /v2iplimitcode

RUN apt-get update && apt install procps -y

COPY ./requirements.txt /v2iplimitcode/

RUN pip install --no-cache-dir --upgrade -r /v2iplimitcode/requirements.txt

COPY . /v2iplimitcode

RUN chmod +x api.py

CMD ["python", "api.py"]