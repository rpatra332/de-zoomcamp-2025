from time import time
import logging as LOG
import pyarrow as pa
from pyarrow.parquet import ParquetFile
from sqlalchemy import create_engine
import argparse
import requests


def download_file(file_url, file_name):
    try:
        response = requests.get(file_url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        LOG.error(f"Download Error: \n{e}")


def main(params):
    LOG.info("Parsing input params")
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    file_name = "yellow_taxi_data.parquet"

    try:
        LOG.info("Starting Ingestion Pipeline")

        LOG.info("Downloading data file for ingestion")
        download_file(url, file_name)
        LOG.info("Download complete")

        LOG.info("Connecting to Destination DB")
        engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{db}")
        conn = engine.connect()
        LOG.info("Connected to Destination DB")

        LOG.info("Started Loading Data")
        pf = ParquetFile(file_name)
        pq_iter = pf.iter_batches(batch_size=100000)

        for batch_no, pq_batch in enumerate(pq_iter):
            t_start = time()
            df = pa.Table.from_batches([pq_batch]).to_pandas()
            df.to_sql(name=table_name, con=conn, if_exists="append")
            t_end = time()
            LOG.info(
                f"Batch {batch_no} took {(t_end - t_start)} seconds to load")

        LOG.info("Ingestion Pipeline Complete")

    except Exception as e:
        LOG.error(e)
        LOG.error("Ingestion Pipeline Failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest Data to Postgres")
    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument(
        "--table-name", help="name of table where data to be written in postgres")
    parser.add_argument("--url", help="url of the parquet file")

    LOG.basicConfig(
        level=LOG.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    args = parser.parse_args()
    main(args)
