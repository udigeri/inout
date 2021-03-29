FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "run.py", "-e", "development"]
EXPOSE 80