FROM python:3.12.6-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DB_HOST=$DB_HOST
ENV DB_NAME=$DB_NAME
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_PORT=$DB_PORT
ENV DB_USER=$DB_USER

EXPOSE 8000

CMD ["python", "consult.py"]
