import dynamics
import server
import threading
import sys
import os
from models.dynamics_db import DYNAMICS_DB
from models.statics_db import STATICS_DB
from models.builds_db import BUILDS_DB

def sort():
    import sorting, statics

    sorting.init()
    while True:
        statics.update_champions()
        statics.update_items()
        statics.update_summoner()
        statics.update_maps()
        statics.update_runes()
        sorting.sort_all()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

serverProcess = threading.Thread(target=server.start_server)
serverProcess.daemon = True
serverProcess.start()

sortingProcess = threading.Thread(target=sort)
sortingProcess.daemon = True
sortingProcess.start()

while True:
    try:
        dynamics.clean_builds()
        if(dynamics.update_builds()):
            continue
        dynamics.update_summoner()
        dynamics.update_matches()
    except KeyboardInterrupt:
        DYNAMICS_DB.stop()
        STATICS_DB.stop()
        BUILDS_DB.stop()
        sys.exit()
    except Exception as exc:
        print("Exception:")
        print(exc)
        continue