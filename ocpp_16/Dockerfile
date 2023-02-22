FROM tiangolo/uvicorn-gunicorn:python3.8-slim
RUN apt-get update
WORKDIR /www
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /app
CMD ["python", "main.py"]
EXPOSE 443 9002