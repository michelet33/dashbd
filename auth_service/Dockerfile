FROM tiangolo/uvicorn-gunicorn:python3.8-slim
RUN apt-get update
RUN apt-get install -y nmap
WORKDIR /www
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8080
#CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]