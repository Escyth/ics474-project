FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron \
 && pip install pandas scikit-learn sqlalchemy trino

COPY revenue_prediction.py .
COPY cron.sh .

RUN chmod +x cron.sh

CMD ["sh", "cron.sh"]