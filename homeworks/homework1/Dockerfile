FROM python:3.12.8
RUN pip install pandas psycopg2 python-dotenv sqlalchemy
WORKDIR /app
COPY .env .env
COPY pipeline.py pipeline.py
COPY data/ data/
ENTRYPOINT [ "python", "pipeline.py" ]