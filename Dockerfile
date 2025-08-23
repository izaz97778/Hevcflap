FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN chmod +x start.sh && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8080

CMD ["bash", "start.sh"]
