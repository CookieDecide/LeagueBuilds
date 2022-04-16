import lcu
import threading
import statics

champ_select_event = threading.Event()

def LCU_Loop(champ_select_event):
    lcu.start(champ_select_event)

def gui_start(champ_select_event):
    import gui
    gui.start(champ_select_event)

def run_gui():
    serverProcess = threading.Thread(name='GUI-Thread', target=gui_start, args=(champ_select_event,))
    serverProcess.daemon = False
    serverProcess.start()

def run_lcu():
    serverProcess = threading.Thread(name='LCU-Thread', target=LCU_Loop, args=(champ_select_event,))
    serverProcess.daemon = True
    serverProcess.start()

statics.update_champions()
statics.update_items()
statics.update_summoner()
statics.update_maps()
statics.update_runes()

run_gui()

run_lcu()