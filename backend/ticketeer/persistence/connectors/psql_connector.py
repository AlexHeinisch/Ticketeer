import psycopg2
from flask import current_app

class PostgresConnector():

    def __init__(self):
        self._conn = psycopg2.connect(
            host=current_app.config['DB_HOST'],
            database=current_app.config['DB_DATABASE'],
            user=current_app.config['DB_USERNAME'],
            password=current_app.config['DB_PASSWORD'])
        self._conn.autocommit = True
    
    def get_conn(self):
        return self._conn