import peewee as pw
import os
from playhouse.sqliteq import SqliteQueueDatabase

if (not os.path.exists('../DB')):
    os.mkdir('../DB')

STATICS_DB = SqliteQueueDatabase('../DB/statics.db')

class CHAMPIONS(pw.Model):
    champion = pw.TextField(primary_key=True, unique=True)

    blurb = pw.TextField()

    id = pw.TextField()

    spell_image_passive = pw.TextField()
    spell_image_q = pw.TextField()
    spell_image_w = pw.TextField()
    spell_image_e = pw.TextField()
    spell_image_r = pw.TextField()

    spell_text_passive = pw.TextField()
    spell_text_q = pw.TextField()
    spell_text_w = pw.TextField()
    spell_text_e = pw.TextField()
    spell_text_r = pw.TextField()

    image_full = pw.TextField()
    image_group = pw.TextField()
    image_h = pw.IntegerField()
    image_sprite = pw.TextField()
    image_w = pw.IntegerField()
    image_x = pw.IntegerField()
    image_y = pw.IntegerField()

    info_attack = pw.IntegerField()
    info_defense = pw.IntegerField()
    info_difficulty = pw.IntegerField()
    info_magic = pw.IntegerField()

    key = pw.TextField()

    name = pw.TextField()

    partype = pw.TextField()

    stats_armor = pw.FloatField()
    stats_armorperlevel = pw.FloatField()
    stats_attackdamage = pw.FloatField()
    stats_attackdamageperlevel = pw.FloatField()
    stats_attackrange = pw.FloatField()
    stats_attackspeed = pw.FloatField()
    stats_attackspeedperlevel = pw.FloatField()
    stats_crit = pw.FloatField()
    stats_critperlevel = pw.FloatField()
    stats_hp = pw.FloatField()
    stats_hpperlevel = pw.FloatField()
    stats_hpregen = pw.FloatField()
    stats_hpregenperlevel = pw.FloatField()
    stats_movespeed = pw.FloatField()
    stats_mp = pw.FloatField()
    stats_mpperlevel = pw.FloatField()
    stats_mpregen = pw.FloatField()
    stats_mpregenperlevel = pw.FloatField()
    stats_spellblock = pw.FloatField()
    stats_spellblockperlevel = pw.FloatField()

    tags = pw.TextField()

    title = pw.TextField()

    version = pw.TextField()


    def __str__(self):
        return self.champion

    class Meta:
        database = STATICS_DB
        db_table = 'champions'

class ITEMS(pw.Model):
    id = pw.TextField(primary_key=True, unique=True)
    colloq = pw.TextField()
    depth = pw.IntegerField()
    description = pw.TextField()
    effect = pw.TextField()
    from_ = pw.TextField()
    gold = pw.TextField()
    image = pw.TextField()
    into = pw.TextField()
    maps = pw.TextField()
    name = pw.TextField()
    plaintext = pw.TextField()
    stacks = pw.IntegerField()
    stats = pw.TextField()
    tags = pw.TextField()

    def __str__(self):
        return self.name

    class Meta:
        database = STATICS_DB
        db_table = 'items'

class SUMMONER(pw.Model):
    main_id = pw.TextField(primary_key=True, unique=True)
    cooldown = pw.TextField()
    cooldownBurn = pw.TextField()
    cost = pw.TextField()
    costBurn = pw.TextField()
    costType = pw.TextField()
    datavalues = pw.TextField()
    description = pw.TextField()
    effect = pw.TextField()
    effectBurn = pw.TextField()
    id = pw.TextField()
    image = pw.TextField()
    key = pw.TextField()
    maxammo = pw.TextField()
    maxrank = pw.IntegerField()
    modes = pw.TextField()
    name = pw.TextField()
    range = pw.TextField()
    rangeBurn = pw.TextField()
    resource = pw.TextField()
    summonerLevel = pw.IntegerField()
    tooltip = pw.TextField()
    vars = pw.TextField()

    def __str__(self):
        return self.main_id

    class Meta:
        database = STATICS_DB
        db_table = 'summoner'

class MAPS(pw.Model):
    id = pw.TextField(primary_key=True, unique=True)
    MapId = pw.TextField()
    MapName = pw.TextField()
    image = pw.TextField()

    def __str__(self):
        return self.id

    class Meta:
        database = STATICS_DB
        db_table = 'maps'

class RUNES(pw.Model):
    id = pw.IntegerField(primary_key=True, unique=True)
    icon = pw.TextField()
    key = pw.TextField()
    longDesc = pw.TextField()
    name = pw.TextField()
    shortDesc = pw.TextField()

    def __str__(self):
        return self.id

    class Meta:
        database = STATICS_DB
        db_table = 'runes'

class RUNESLOTS(pw.Model):
    rune_1 = pw.ForeignKeyField(RUNES, primary_key=True)
    rune_2 = pw.ForeignKeyField(RUNES)
    rune_3 = pw.ForeignKeyField(RUNES)

    def __str__(self):
        return self.rune_1

    class Meta:
        database = STATICS_DB
        db_table = 'runeslots'

class RUNEKEYS(pw.Model):
    id = pw.IntegerField(primary_key=True, unique=True)
    icon = pw.TextField()
    key = pw.TextField()
    name = pw.TextField()
    slot_1 = pw.ForeignKeyField(RUNESLOTS)
    slot_2 = pw.ForeignKeyField(RUNESLOTS)
    slot_3 = pw.ForeignKeyField(RUNESLOTS)
    slot_4 = pw.ForeignKeyField(RUNESLOTS)

    def __str__(self):
        return self.id

    class Meta:
        database = STATICS_DB
        db_table = 'runekeys'

STATICS_DB.connect()

STATICS_DB.start()
STATICS_DB.create_tables([CHAMPIONS, ITEMS, SUMMONER, MAPS, RUNEKEYS, RUNESLOTS, RUNES])
STATICS_DB.stop()
STATICS_DB.start()