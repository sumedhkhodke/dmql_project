
import psycopg2
import pandas as pd
import psycopg2.extras as extras
# from sqlalchemy import create_engine
from io import StringIO
import numpy as np
import os 
# from psycopg2.extensions import register_adapter, AsIs
# psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

# Here you want to change your database, username & password according to your own values
param_dic = {
    "host"      : "localhost",
    "database"  : "test1",
    "user"      : "postgres",
    "password"  : "neww"
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn

conn = connect(param_dic)

data = {'user_id':1,'user_sel_1':1,'user_sel_2':1,'user_sel_3':1,'sum_of_scores':80}
df = pd.DataFrame(data, index=[0])
df = df.convert_dtypes()

def execute_many(conn, df, table):
    """
    Using cursor.executemany() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    print(cols)
    print(table)
    query  = "INSERT INTO "+table+"("+cols+") VALUES(%s,%s,%s,%s,%s)" 
    # query  = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % (table, cols)
    cursor = conn.cursor()
    try:
        cursor.executemany(query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_many() done")
    cursor.close()

x = execute_many(conn, df, 'user_selection')

