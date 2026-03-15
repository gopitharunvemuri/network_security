FROM python:3.13-slim
WORKDIR /network_security
COPY . .

RUN apt-get update && apt-get install -y awscli
RUN pip install -r requirements.txt
CMD ["python", "app.py"]