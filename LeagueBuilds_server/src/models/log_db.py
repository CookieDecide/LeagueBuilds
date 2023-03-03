import peewee as pw
import os
from playhouse.sqliteq import SqliteQueueDatabase

if (not os.path.exists('../DB')):
    os.mkdir('../DB')

LOG_DB = SqliteQueueDatabase('../DB/log.db',
                            autostart=False)

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

class PLAYER(pw.Model):
    time = pw.TextField(primary_key=True)
    ip = pw.TextField(index=True)
    port = pw.TextField()
    summonername = pw.TextField()

    def __str__(self):
        return self.summonerid

    class Meta:
        database = LOG_DB
        db_table = 'player'

LOG_DB.start()
LOG_DB.connect()
LOG_DB.create_tables([CONNECTION, PLAYER])
LOG_DB.close()
LOG_DB.connect()