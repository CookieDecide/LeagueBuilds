import lcu
import statics
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

statics.update_champions()
statics.update_items()
statics.update_summoner()
statics.update_maps()
statics.update_runes()

lcu.start()