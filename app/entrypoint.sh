PG_DSN_MIGRATION=postgresql+psycopg2://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:5432/${PG_DB} sh migrate.sh
python app.py