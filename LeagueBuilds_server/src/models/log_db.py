import peewee as pw
import os
from playhouse.sqliteq import SqliteQueueDatabase

if (not os.path.exists('../DB')):
    os.mkdir('../DB')

LOG_DB = SqliteQueueDatabase('../DB/log.db')

class CONNECTION(pw.Model):
    time = pw.TextField(primary_key=True)
    ip = pw.TextField(index=True)
    port = pw.TextField()
    championId = pw.TextField()
    champion = pw.TextField()
    position = pw.TextField()

    def __str__(self):
        return self.championId

    class Meta:
        database = LOG_DB
        db_table = 'connection'

LOG_DB.connect()

LOG_DB.start()
LOG_DB.create_tables([CONNECTION])
LOG_DB.stop()
LOG_DB.start()