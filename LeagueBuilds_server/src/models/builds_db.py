import peewee as pw
import os
from playhouse.sqliteq import SqliteQueueDatabase

if not os.path.exists("../DB"):
    os.mkdir("../DB")

BUILDS_DB = SqliteQueueDatabase("../DB/builds.db", autostart=False)


class FINALBUILDS(pw.Model):
    championId = pw.TextField()
    runes = pw.TextField()
    summ = pw.TextField()
    item = pw.TextField()
    start_item = pw.TextField()
    item_build = pw.TextField()
    skill_order = pw.TextField()
    position = pw.TextField()
    boots = pw.TextField()

    def __str__(self):
        return self.championId

    class Meta:
        database = BUILDS_DB
        db_table = "finalbuilds"
        primary_key = pw.CompositeKey("championId", "position")


BUILDS_DB.start()
BUILDS_DB.connect()
BUILDS_DB.create_tables([FINALBUILDS])
BUILDS_DB.close()
BUILDS_DB.connect()
