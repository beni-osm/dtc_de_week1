import os

import pandas as pd
import requests
import psycopg2
import psycopg2.extras as extras
import gzip
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(database=os.environ.get('POSTGRES_NAME'),
                        user=os.environ.get('POSTGRES_USER'),
                        password=os.environ.get('POSTGRES_PASSWORD'),
                        host=os.environ.get('POSTGRES_HOST'),
                        port=os.environ.get('POSTGRES_PORT'))

def download_data(url, type = None):
    response = requests.get(url)
    with open(url.split('/')[-1], "wb") as f:
        f.write(response.content)
    if type == 'gzip':
        with gzip.open(url.split('/')[-1], 'rb') as f_in:
            with open('.'.join(url.split('/')[-1].split('.')[:-1]), 'wb') as f_out:
                f_out.write(f_in.read())

def execute_values(conn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()


gree_taxi_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
taxi_zone_url = "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
download_data(gree_taxi_url, 'gzip')
download_data(taxi_zone_url)

green_taxi = pd.read_csv('.'.join(gree_taxi_url.split('/')[-1].split('.')[:-1]))
taxi_zone = pd.read_csv(taxi_zone_url.split('/')[-1])
print("Writing Data ....")
execute_values(conn, green_taxi, 'yellow_taxi')
execute_values(conn, taxi_zone, 'taxi_zone')

conn.close()
