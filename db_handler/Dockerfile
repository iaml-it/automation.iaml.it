FROM python:3.8-slim
WORKDIR db_handler
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "app.py"]
