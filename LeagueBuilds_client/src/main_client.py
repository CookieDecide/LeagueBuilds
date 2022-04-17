import lcu, gui
import threading
import statics

def LCU_Loop():
    lcu.start()

def run_lcu():
    serverProcess = threading.Thread(name='LCU-Thread', target=LCU_Loop)
    serverProcess.daemon = True
    serverProcess.start()

statics.update_champions()
statics.update_items()
statics.update_summoner()
statics.update_maps()
statics.update_runes()

run_lcu()

gui.start()