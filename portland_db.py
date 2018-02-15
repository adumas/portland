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
            id integer NOT NULL PRIMARY KEY,
            name TEXT NOT NULL, 
            email TEXT,
            role TEXT NOT NULL,
            message_id VARCHAR(16), FOREIGN KEY(message_id) REFERENCES messages(id))"""
        self.conn.execute(people_schema)
        self.conn.commit()

    def __create_message_table(self):
        message_schema = """CREATE TABLE IF NOT EXISTS messages
                (id VARCHAR(16) NOT NULL PRIMARY KEY, 
                subject TEXT,
                from_ TEXT,
                num_recipients INTEGER,
                date TEXT,
                internalDate VARCHAR(13),
                snippet TEXT,
                body TEXT)"""
        self.conn.execute(message_schema)
        self.conn.commit()

    def get_insert_string(self,table,field_additions):
        field_add_string = ''.join(['{},'.format(f) for f in field_additions]).strip(',')
        sql_spec_string = ''.join(['?,' for i in xrange(len(field_additions))]).strip(',')
        return 'INSERT INTO {}({}) VALUES({})'.format(table,field_add_string, sql_spec_string)

    def add_message(self,msg=None):
        """
        Add a message into the messages table
        :param msg:
        :return: message id
        """
        if msg is None:
            return

        field_additions = ('id','subject','from_','num_recipients','date','internalDate','snippet','body')
        sql_insert = self.get_insert_string('messages', field_additions)

        msg_vector = []
        for field in field_additions:
            value = getattr(msg,field)
            if field == 'from_':
                sender = value[0]
                value = u'{}'.format(sender)

            if field == 'date':
                value = u'{}'.format(value)

            msg_vector.append(value)

        print msg_vector

        cur = self.conn.cursor()
        cur.execute(sql_insert, msg_vector)
        #msg_id = cur.lastrowid

    def add_people(self,msg):
        people_fields = ['from_','to','cc']
        for field in people_fields:
            people = getattr(msg,field)
            
            if field == 'from_':
                role = 'from'
            else:
                role = 'to'

            for person in people:
                print person
                self.add_person(id,role,person)

    def add_person(self,id,role,person):
        field_additions = ('message_id','role','name','address')
        sql_insert = self.get_insert_string('people',field_additions)
        person_vector = (id,role,person.name,person.address)

        cur = self.conn.cursor()
        cur.execute(sql_insert, person_vector)


from gmail_message import Gmail
from gmail_message import Message

if __name__ == "__main__":
    db = PortlandDB()
    db.connect(syncdb=True)

    messages = db.conn.execute("SELECT count(rowid) FROM messages").fetchone()[0]
    print "There are now %i messages" % messages

    G = Gmail()
    print "getting message"
    messages = G.search_messages('subject: "Re: Portland"')
    test_message = G.get_message(messages[0]['id'])
    print "OK"
    print "adding message to db"
    db.add_message(test_message)
    messages = db.conn.execute("SELECT count(rowid) FROM messages").fetchone()[0]
    print "There are now %i messages" % messages

    results = db.conn.execute("SELECT * FROM messages").fetchone()[0]
    print results

    db.close()
