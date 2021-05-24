import psycopg2
import os
         
tables = ['customer',
'lineitem',
'nation',
'orders',
'part',
'partsupp',
'region',
'supplier']

conn_string = "host='localhost' port=54320 dbname='my_database' user='root' password='postgres'" 

with psycopg2.connect(conn_string) as conn, conn.cursor() as cursor:
    for t in tables:
        q = "COPY %s TO STDOUT WITH DELIMITER ',' CSV HEADER;" % t
        with open("%s.csv" % t, 'w') as f:
            cursor.copy_expert(q, f)

conn_string2 = "host='localhost' port=5433 dbname='my_database' user='root' password='postgres'" 

with psycopg2.connect(conn_string2) as conn, conn.cursor() as cursor:
    for t in tables:
        q = "COPY %s from STDIN WITH DELIMITER ',' CSV HEADER;" % t
        with open("%s.csv" % t, 'r') as f:
            cursor.copy_expert(q, f)
        cursor.execute("select count(*) from %s" % t)
        print("%s: %d" % (t,cursor.fetchall()[0][0]))
        os.remove("%s.csv" % t)