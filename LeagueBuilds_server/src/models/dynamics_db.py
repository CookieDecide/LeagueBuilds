import peewee as pw
import os
from playhouse.sqliteq import SqliteQueueDatabase

if (not os.path.exists('../DB')):
    os.mkdir('../DB')

DYNAMICS_DB = SqliteQueueDatabase('../DB/dynamics.db',
                                autostart=False)

class MATCHES(pw.Model):
    matchId = pw.TextField(primary_key=True, unique=True)

    def __str__(self):
        return self.matchId

    class Meta:
        database = DYNAMICS_DB
        db_table = 'matches'

class SUMMONER(pw.Model):
    summonerId = pw.TextField(primary_key=True, unique=True)
    summonerName = pw.TextField()
    puuid = pw.TextField()


    def __str__(self):
        return self.summonerId

    class Meta:
        database = DYNAMICS_DB
        db_table = 'summoner'

class BUILDS(pw.Model):
    matchId = pw.TextField()
    gameEndTimestamp = pw.TextField()

    championId = pw.TextField(index=True)
    championName = pw.TextField()
    teamPosition = pw.TextField()
    individualPosition = pw.TextField()
    lane = pw.TextField()

    item0 = pw.TextField()
    item1 = pw.TextField()
    item2 = pw.TextField()
    item3 = pw.TextField()
    item4 = pw.TextField()
    item5 = pw.TextField()
    item6 = pw.TextField()

    start_items = pw.TextField()
    items = pw.TextField()
    skills = pw.TextField()

    summoner1Id = pw.IntegerField()
    summoner2Id = pw.IntegerField()

    win = pw.BooleanField()

    defense = pw.IntegerField()
    flex = pw.IntegerField()
    offense = pw.IntegerField()

    primaryStyle = pw.IntegerField()
    primaryPerk1 = pw.IntegerField()
    primaryPerk2 = pw.IntegerField()
    primaryPerk3 = pw.IntegerField()
    primaryPerk4 = pw.IntegerField()

    subStyle = pw.IntegerField()
    subPerk1 = pw.IntegerField()
    subPerk2 = pw.IntegerField()


    def __str__(self):
        return self.championId

    class Meta:
        database = DYNAMICS_DB
        db_table = 'builds'
        primary_key = pw.CompositeKey('matchId', 'championId')
        indexes=(
            (('championId', 'teamPosition'), False),
        )

class ARAM(pw.Model):
    matchId = pw.TextField()
    gameEndTimestamp = pw.TextField()

    championId = pw.TextField(index=True)
    championName = pw.TextField()
    teamPosition = pw.TextField()
    individualPosition = pw.TextField()
    lane = pw.TextField()

    item0 = pw.TextField()
    item1 = pw.TextField()
    item2 = pw.TextField()
    item3 = pw.TextField()
    item4 = pw.TextField()
    item5 = pw.TextField()
    item6 = pw.TextField()

    start_items = pw.TextField()
    items = pw.TextField()
    skills = pw.TextField()

    summoner1Id = pw.IntegerField()
    summoner2Id = pw.IntegerField()

    win = pw.BooleanField()

    defense = pw.IntegerField()
    flex = pw.IntegerField()
    offense = pw.IntegerField()

    primaryStyle = pw.IntegerField()
    primaryPerk1 = pw.IntegerField()
    primaryPerk2 = pw.IntegerField()
    primaryPerk3 = pw.IntegerField()
    primaryPerk4 = pw.IntegerField()

    subStyle = pw.IntegerField()
    subPerk1 = pw.IntegerField()
    subPerk2 = pw.IntegerField()


    def __str__(self):
        return self.championId

    class Meta:
        database = DYNAMICS_DB
        db_table = 'aram'
        primary_key = pw.CompositeKey('matchId', 'championId')

DYNAMICS_DB.start()
DYNAMICS_DB.connect()
DYNAMICS_DB.create_tables([MATCHES, SUMMONER, BUILDS, ARAM])
DYNAMICS_DB.close()
DYNAMICS_DB.connect()