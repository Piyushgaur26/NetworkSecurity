FROM python:3.11-slim-bookworm
WORKDIR /app
COPY . /app
RUN apt update && apt install awscli -y 
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
