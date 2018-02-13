import sqlite3
import os
from sqlite3 import Error

class PortlandDB():
    def __init__(self):
        self.db = 'portland.db'
        self.conn = None
        self.__open = False


    def connect(self,syncdb=False):
        """
        Connects to the database and ensures there are tables.
        """
        if not os.path.exists(self.db):
            syncdb = True

        self.conn = sqlite3.connect(self.db)
        self.__open = True
        if syncdb:
            self.create_tables()

    def close(self):
        if self.__open:
            self.conn.close()

    def create_tables(self):
        self.__create_message_table()
        self.__create_people_table()

    def __create_people_table(self):
        people_schema = """CREATE TABLE IF NOT EXISTS people ( 
            name TEXT NOT NULL, 
            email TEXT,
            role TEXT NOT NULL,
            message_id VARCHAR(16), FOREIGN KEY(message_id) REFERENCES messages(message_id))"""
        self.conn.execute(people_schema)
        self.conn.commit()

    def __create_message_table(self):
        # - message schema
            # - subject
            # - messageid
            # - snippet
            # - n_recipients
            # - sender
            # - date
            # - internalDate
            # - attachments
            # - body
        message_schema = """CREATE TABLE IF NOT EXISTS messages
                (id INTEGER NOT NULL PRIMARY KEY,
                message_id VARCHAR(16), 
                subject TEXT,
                snippet TEXT,
                num_recipients INTEGER,
                sender TEXT,
                date TEXT,
                internalDate INT,
                body TEXT)"""
        self.conn.execute(message_schema)
        self.conn.commit()

    def add_message(self,msg):
        pass

    def add_person(self,person):
        pass


if __name__ == "__main__":
    db = PortlandDB()
    db.connect(syncdb=True)

    messages = db.conn.execute("SELECT count(rowid) FROM messages").fetchone()[0]
    print "There are now %i messages" % messages
    db.close()