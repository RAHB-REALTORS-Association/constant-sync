import pyodbc

class Database:
    def __init__(self, server, database, username, password, query):
        self.connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};UID={username};PWD={password};TrustServerCertificate=yes"
        self.connection = pyodbc.connect(self.connection_string)
        self.query = query

    def get_contacts(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.query)
            contacts = [dict(row) for row in cursor.fetchall()]
        return contacts

    def close(self):
        self.connection.close()
    