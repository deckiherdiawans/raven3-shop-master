import psycopg2 as pg2
import sys


class Postgre(object):
    def connection(self):
        pgconn = pg2.connect(
            user="revota",
            password="r3vot4",
            database="revota",
            host="localhost",
            port="5432",
        )
        if not pgconn:
            sys.exit()
        else:
            return pgconn