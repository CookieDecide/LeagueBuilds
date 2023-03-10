import dynamics
import server
import threading
import sys
import os, time
from models.dynamics_db import DYNAMICS_DB
from models.statics_db import STATICS_DB
from models.builds_db import BUILDS_DB
from models.log_db import LOG_DB

def close_db():
    DYNAMICS_DB.execute_sql("pragma wal_checkpoint;")
    DYNAMICS_DB.close()
    DYNAMICS_DB.stop()
    STATICS_DB.execute_sql("pragma wal_checkpoint;")
    STATICS_DB.close()
    STATICS_DB.stop()
    BUILDS_DB.execute_sql("pragma wal_checkpoint;")
    BUILDS_DB.close()
    BUILDS_DB.stop()
    LOG_DB.execute_sql("pragma wal_checkpoint;")
    LOG_DB.close()
    LOG_DB.stop()
    print("stopped")
    while (not DYNAMICS_DB.is_stopped() or not STATICS_DB.is_stopped() or not BUILDS_DB.is_stopped() or not LOG_DB.is_stopped()):
        time.sleep(1)
        print("Waiting on DB")

def open_db():
    DYNAMICS_DB.start()
    DYNAMICS_DB.connect(reuse_if_open=True)
    STATICS_DB.start()
    STATICS_DB.connect(reuse_if_open=True)
    BUILDS_DB.start()
    BUILDS_DB.connect(reuse_if_open=True)
    LOG_DB.start()
    LOG_DB.connect(reuse_if_open=True)
    print("started")
    while (not DYNAMICS_DB.is_connection_usable() or not STATICS_DB.is_connection_usable() or not BUILDS_DB.is_connection_usable() or not LOG_DB.is_connection_usable()):
        time.sleep(1)
        print("Waiting on DB")

def sort():
    import sorting, statics

    sorting.init()
    statics.update_champions()
    statics.update_items()
    statics.update_summoner()
    statics.update_maps()
    statics.update_runes()
    sorting.sort_pro()


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

serverProcess = threading.Thread(target=server.start_server)
serverProcess.daemon = True
serverProcess.start()

while True:
    try:
        open_db()

        sortingProcess = threading.Thread(target=sort)
        sortingProcess.daemon = True
        sortingProcess.start()
        
        dynamics.clean_builds()
        
        while True:
            if(dynamics.update_builds()):
                continue
            else:
                break
        
        dynamics.update_matches()
        dynamics.update_summoner()

        sortingProcess.join()

        close_db()
        time.sleep(60)
    except KeyboardInterrupt:
        close_db()
        sys.exit()
    except Exception as exc:
        print("Exception:")
        print(exc)
        continue