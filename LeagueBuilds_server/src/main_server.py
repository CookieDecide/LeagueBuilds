import dynamics
import server
import threading
import sys
import os

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
        dynamics.update_builds()
        dynamics.update_matches()
        dynamics.update_summoner()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as exc:
        print("Exception:")
        print(exc)
        continue