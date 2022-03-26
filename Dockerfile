FROM python:3.8-slim
COPY . .
RUN pip install -r requirements.txt
WORKDIR "/src"
CMD ["python3", "main.py"]
