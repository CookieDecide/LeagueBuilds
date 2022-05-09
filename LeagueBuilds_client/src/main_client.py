import lcu, gui, client, version
import threading, time
import statics

def LCU_Loop():
    lcu.start()

def run_lcu():
    serverProcess = threading.Thread(name='LCU-Thread', target=LCU_Loop)
    serverProcess.daemon = True
    serverProcess.start()

def update_check():
    time.sleep(5)
    server_version = client.get_build('','')

    if(version.version != server_version):
        print('new version available')
        gui.update_available(version.version, server_version)
    else:
        print('no new version available')

statics.update_champions()
statics.update_items()
statics.update_summoner()
statics.update_maps()
statics.update_runes()

run_lcu()

updateProcess = threading.Thread(name='LCU-Thread', target=update_check)
updateProcess.daemon = True
updateProcess.start()

gui.start()