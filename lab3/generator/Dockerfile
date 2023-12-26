FROM python:3.11

WORKDIR /app

COPY generator.py .

COPY config.json .

RUN pip install requests

CMD ["python3", "generator.py"]
