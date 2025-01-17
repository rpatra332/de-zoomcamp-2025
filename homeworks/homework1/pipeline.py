import logging as LOG
import time
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values


def config_log():
    """
    Configure the logging level and format.
    """
    LOG.basicConfig(
        level=LOG.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_and_process_taxi_data(chunk_no, df, table, conn):
    """
    Convert datetime columns to datetime objects and insert the chunk into the database.

    Parameters:
    chunk_no (int): The current chunk number.
    df (pd.DataFrame): The current data chunk.
    table (str): The database table name.
    conn (sqlalchemy.engine.Connection): The database connection object.
    """
    s_time = time.time()
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    df.to_sql(table, con=conn, if_exists="append", index=False)
    e_time = time.time()
    LOG.info(
        f"Chunk {chunk_no + 1}: Loaded {len(df)} rows to database@{(e_time - s_time):.3f} seconds")


def read_and_process_zone_date(conn, zone_table, zone_file):
    """
    Read and insert the taxi-zone data to database.

    Parameters:
    conn (sqlalchemy.engine.Connection): The database connection object.
    """
    s_time = time.time()
    zone_df = pd.read_csv(zone_file)
    zone_df.to_sql(zone_table, con=conn, if_exists="replace", index=False)
    e_time = time.time()
    LOG.info(
        f"Loaded taxi-zone data to database@{(e_time - s_time):.3f} seconds")


def etl():
    """
    Execute the ETL pipeline: Extract, Transform, Load.
    """
    try:
        LOG.info("Loading config...")
        config = dotenv_values()

        LOG.info("Connecting to Postgres Database...")
        engine = create_engine(
            f'postgresql://{config["USER"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["DB"]}')
        conn = engine.connect()

        LOG.info("Starting data loading pipeline...")
        LOG.info("Inserting taxi data...")
        df_iter = pd.read_csv(
            config["DATAFILE"], iterator=True, chunksize=int(config["CHUNKSIZE"]), compression="gzip")

        for chunk_no, df in enumerate(df_iter):
            read_and_process_taxi_data(chunk_no, df, config["TABLE"], conn)
        LOG.info("Taxi data insertion complete.")

        LOG.info("Inserting taxi-zone data...")
        read_and_process_zone_date(
            conn, config["ZONETABLE"], config["ZONEFILE"])
        LOG.info("Taxi-zone data insertion complete.")

        LOG.info("Data loading pipeline completed successfully.")

    except Exception as e:
        LOG.error(f"An error occurred: {e}")
        LOG.error("Data loading pipeline failed")
    finally:
        # Ensure the connection is closed even if an exception occurs
        if conn:
            conn.close()
            LOG.info("Database connection closed.")


if __name__ == "__main__":
    config_log()
    etl()
