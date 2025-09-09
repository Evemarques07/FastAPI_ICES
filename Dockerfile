FROM python:3.11-slim

ENV TZ=America/Sao_Paulo
RUN apt-get update && apt-get install -y gcc libpq-dev tzdata && rm -rf /var/lib/apt/lists/*
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code
COPY . /code


RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
