from configparser import ConfigParser
config_parser = ConfigParser()

config_parser.read('config.ini')

api_key = config_parser.get('main', 'api_key')

import_runes = config_parser.getboolean('import', 'runes')
import_items = config_parser.getboolean('import', 'items')
import_summs = config_parser.getboolean('import', 'summs')
position_flash = config_parser.getint('import', 'flash')

gui_darkmode = config_parser.getboolean('gui', 'darkmode')

def set_import_runes(import_runes):
    config_parser.set('import', 'runes', str(import_runes))
    with open('config.ini', 'w') as f:
        config_parser.write(f)

def set_import_items(import_items):
    config_parser.set('import', 'items', str(import_items))
    with open('config.ini', 'w') as f:
        config_parser.write(f)

def set_import_summs(import_summs):
    config_parser.set('import', 'summs', str(import_summs))
    with open('config.ini', 'w') as f:
        config_parser.write(f)

def set_import_flash(import_flash):
    config_parser.set('import', 'flash', str(import_flash))
    with open('config.ini', 'w') as f:
        config_parser.write(f)


def set_gui_darkmode(darkmode):
    config_parser.set('gui', 'darkmode', str(darkmode))
    with open('config.ini', 'w') as f:
        config_parser.write(f)