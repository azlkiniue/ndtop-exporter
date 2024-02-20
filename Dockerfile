FROM python:3-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ARG BIND=127.0.0.1
ARG PORT=8000
ARG INTERVAL=1.0
ARG HOSTNAME=localhost
ENV BIND=${BIND}
ENV PORT=${PORT}
ENV INTERVAL=${INTERVAL}
ENV HOSTNAME=${HOSTNAME}

CMD python -m nvitop_exporter --bind ${BIND} --port ${PORT} --interval ${INTERVAL} --hostname ${HOSTNAME}