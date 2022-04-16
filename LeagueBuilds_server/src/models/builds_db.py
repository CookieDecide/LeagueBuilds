import peewee as pw
import os

if (not os.path.exists('../DB')):
    os.mkdir('../DB')

BUILDS_DB = pw.SqliteDatabase('../DB/builds.db', check_same_thread=False)

class FINALBUILDS(pw.Model):
    championId = pw.TextField()
    runes = pw.TextField()
    summ = pw.TextField()
    item = pw.TextField()
    start_item = pw.TextField()
    item_build = pw.TextField()
    skill_order = pw.TextField()
    position = pw.TextField()


    def __str__(self):
        return self.summonerId

    class Meta:
        database = BUILDS_DB
        db_table = 'finalbuilds'
        primary_key = pw.CompositeKey('championId', 'position')

BUILDS_DB.connect()

BUILDS_DB.create_tables([FINALBUILDS])