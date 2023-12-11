FROM python:3.9-alpine
WORKDIR /exam
COPY requirements.txt .
RUN pip install -r requirements.txt
# Set the environment variable
ENV CASSANDRA_HOST="127.0.0.1"
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]