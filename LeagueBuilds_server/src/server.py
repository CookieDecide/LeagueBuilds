from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from models.builds_db import FINALBUILDS
from models.statics_db import CHAMPIONS
import version
from models.log_db import CONNECTION, PLAYER
import logging, os

if (not os.path.exists('../../../log')):
    os.mkdir('../../../log')

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('../../../log/server.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

app = Flask(__name__)
api = Api(app)

def start_server():
    app.run(host='0.0.0.0', port=12345)

class Builds(Resource):
    def get(self, champion, position=''):
        ip = str(request.remote_addr)
        port = str(12345)

        logger.info(f'{ip}\t{port}\t{request.headers.get("Summoner")}\t{champion}\t{position}')

        PLAYER.insert(
            time = datetime.now(),
            ip = ip,
            port = port,
            summonername = request.headers.get("Summoner")
        ).execute()

        if(position!=''):
            build = FINALBUILDS.get_or_none(
                FINALBUILDS.championId == champion,
                FINALBUILDS.position == str(position).lower()
            )
            if(not build):
                build = FINALBUILDS.get_or_none(
                    FINALBUILDS.championId == champion,
                    FINALBUILDS.position == ""
                )
        else:
            build = FINALBUILDS.get_or_none(
                FINALBUILDS.championId == champion,
                FINALBUILDS.position == ""
            )

        buffer = {}
        buffer["championId"] =  build.championId
        buffer["runes"] =  build.runes
        buffer["summ"] =  build.summ
        buffer["item"] =  build.item
        buffer["start_item"] =  build.start_item
        buffer["item_build"] =  build.item_build
        buffer["skill_order"] =  build.skill_order
        buffer["position"] =  build.position
        buffer["boots"] =  build.boots
        buffer["champion"] =  CHAMPIONS.get(CHAMPIONS.key == build.championId).champion

        CONNECTION.insert(
            time = datetime.now(),
            ip = ip,
            port = port,
            championId = buffer["championId"],
            champion = buffer["champion"],
            position = buffer["position"]
        ).execute()

        return buffer

class Version(Resource):
    def get(self):
        return version.version

api.add_resource(Builds, '/builds/<champion>/<position>', '/builds/<champion>')
api.add_resource(Version, '/version')
