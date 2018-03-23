import psycopg2
from pprint import pprint

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(dbname='postgres', user = 'postgres', password = '123', host = '127.0.0.1', port = '5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Cannot connect")

    def query_all(self):
        self.cursor.execute("SELECT * FROM datatable")
        cats = self.cursor.fetchall()
        for cat in cats:
            pprint("Eah: {0}".format(cat))

if __name__=='__main__':
    database_connection = DatabaseConnection()
    database_connection.query_all()