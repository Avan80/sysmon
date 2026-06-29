FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY systems_monitor.py .

RUN mkdir -p /var/log/sysmon

CMD ["python3", "systems_monitor.py"]