import lcu
import statics
import os

def LCU_Loop():
    statics.update_champions()
    statics.update_items()
    statics.update_summoner()
    statics.update_maps()
    statics.update_runes()

    lcu.start()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

LCU_Loop()