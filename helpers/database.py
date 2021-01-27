import pyodbc as py
import sys
from helpers.config import Config

class Database(object):
    def __init__(self):
        self.config = Config().get()

    def koneksi(self):
        conn = py.connect("DSN=" + self.config['dsn'] + ";uid=" + self.config['username'] + ";pwd=" + self.config['password'], autocommit=True)
        if not conn:
            sys.exit()
        else:
            return conn
