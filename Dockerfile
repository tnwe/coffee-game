FROM python:3.11-slim

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r backend/requirements.txt

RUN chmod +x deploy/start.sh

CMD ["bash", "deploy/start.sh"]
