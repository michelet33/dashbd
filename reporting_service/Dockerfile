FROM tiangolo/uvicorn-gunicorn:python3.8-slim
RUN apt-get update
WORKDIR /www
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]