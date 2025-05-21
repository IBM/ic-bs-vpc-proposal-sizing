FROM python:3.12-slim

LABEL  maintainer="IBM <jorgehernandezramirez@ibm.com>"

WORKDIR /app

COPY requirements.txt .
COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]