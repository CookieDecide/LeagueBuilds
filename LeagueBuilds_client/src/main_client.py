import lcu
import statics
import os
import threading

def LCU_Loop():
    statics.update_champions()
    statics.update_items()
    statics.update_summoner()
    statics.update_maps()
    statics.update_runes()

    lcu.start()

def gui_start():
    import gui
    leagueBuildsApp = gui.LeagueBuildsApp()
    leagueBuildsApp.run()

def run_gui():
    serverProcess = threading.Thread(target=gui_start)
    serverProcess.daemon = False
    serverProcess.start()

def run_lcu():
    serverProcess = threading.Thread(target=LCU_Loop)
    serverProcess.daemon = True
    serverProcess.start()

#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)
#os.chdir(dname)

run_gui()

run_lcu()