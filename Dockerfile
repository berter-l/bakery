FROM python:3.12-alpine3.23
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --force-reinstall redis==7.4.0 && \
    pip install --no-cache-dir -r requirements.txt
