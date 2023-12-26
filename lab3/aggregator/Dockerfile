FROM python:3.11

WORKDIR /app

COPY aggregator.py .

RUN pip install flask requests

CMD ["python3", "aggregator.py"]
