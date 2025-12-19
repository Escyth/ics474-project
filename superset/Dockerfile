FROM apache/superset:latest

USER root

# Install Trino driver directly into Superset's venv site-packages
RUN pip install --no-cache-dir \
    psycopg2-binary \
    sqlalchemy-trino \
    --target=/app/.venv/lib/python3.10/site-packages

COPY superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py

USER superset
ENTRYPOINT ["/superset-init.sh"]
