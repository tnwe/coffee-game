FROM python:3.11-slim

# install node
RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r backend/requirements.txt

RUN chmod +x deploy/start.sh

CMD ["bash", "deploy/start.sh"]
