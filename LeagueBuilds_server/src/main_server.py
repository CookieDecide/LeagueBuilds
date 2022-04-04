import dynamics
import server
import threading
import sys
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

serverProcess = threading.Thread(target=server.start_server)
serverProcess.daemon = True
serverProcess.start()

while True:
    try:
        dynamics.update_builds()
        dynamics.update_summoner()
        dynamics.update_matches()
    except KeyboardInterrupt:
        sys.exit()
    #except Exception as exc:
    #    print("Exception:")
    #    print(exc)
    #    continue