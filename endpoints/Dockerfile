# Dockerfile for deploying LazyTeacher endpoints in a container
# Authors: Ilan ALIOUCHOUCHE & Ilyes DJERFAF

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY .env /app/.env
RUN chmod 777 /app/.env

COPY data/corrected_dict.json /app/data/corrected_dict.json

COPY endpoints /app/endpoints
RUN rm -rf /app/endpoints/README.md

EXPOSE 8000

CMD ["python", "endpoints/endpoint.py"]