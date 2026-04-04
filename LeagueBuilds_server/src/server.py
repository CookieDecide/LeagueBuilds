from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from models.builds_db import FINALBUILDS
from models.statics_db import CHAMPIONS
import version
from models.log_db import CONNECTION, PLAYER
import logging, os
import ast

if not os.path.exists("../../../log"):
    os.mkdir("../../../log")

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("../../../log/server.log")
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - T:%(thread)d/%(threadName)s - %(message)s")
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - T:%(thread)d/%(threadName)s - %(message)s")
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

app = Flask(__name__)
api = Api(app)


def start_server():
    host = "127.0.0.1"
    port = 12345
    force_dev_server = os.getenv("LEAGUEBUILDS_DEV_SERVER", "0") == "1"
    flask_env = os.getenv("FLASK_ENV", "production").lower()
    use_dev_server = force_dev_server or flask_env in {"development", "dev"}

    if use_dev_server:
        logger.info(f"Starting Flask dev server on {host}:{port}")
        app.run(host=host, port=port, debug=True, use_reloader=False)
        return

    try:
        from waitress import serve
    except ImportError:
        logger.warning(
            "waitress is not installed; falling back to Flask dev server. "
            "Install waitress for production usage."
        )
        app.run(host=host, port=port, debug=False, use_reloader=False)
        return

    thread_count = int(os.getenv("LEAGUEBUILDS_SERVER_THREADS", "8"))
    logger.info(f"Starting production server (waitress) on {host}:{port} with {thread_count} threads")
    serve(app, host=host, port=port, threads=thread_count)


class Builds(Resource):
    def get(self, champion, position=""):
        ip = str(request.remote_addr)
        port = str(12345)

        summoner = request.headers.get("Summoner")

        if not summoner:
            summoner = "INCOGNITO"

        logger.info(f"{ip}\t{port}\t{summoner}\t{champion}\t{position}")

        PLAYER.insert(
            time=datetime.now(), ip=ip, port=port, summonername=summoner
        ).execute()

        if position != "":
            build = FINALBUILDS.get_or_none(
                FINALBUILDS.championId == champion,
                FINALBUILDS.position == str(position).lower(),
            )
            if not build:
                build = FINALBUILDS.get_or_none(
                    FINALBUILDS.championId == champion, FINALBUILDS.position == ""
                )
        else:
            build = FINALBUILDS.get_or_none(
                FINALBUILDS.championId == champion, FINALBUILDS.position == ""
            )

        buffer = {}
        buffer["championId"] = build.championId
        rune = ast.literal_eval(build.runes)
        if isinstance(rune, list):
            rune = rune[0]
        buffer["runes"] = str(rune)
        buffer["summ"] = build.summ
        buffer["item"] = build.item
        buffer["start_item"] = build.start_item
        buffer["item_build"] = build.item_build
        buffer["skill_order"] = build.skill_order
        buffer["position"] = build.position
        buffer["boots"] = build.boots
        buffer["champion"] = CHAMPIONS.get(CHAMPIONS.key == build.championId).champion
        buffer["champ_winrate"] = build.champ_winrate
        buffer["champ_pickrate"] = build.champ_pickrate

        CONNECTION.insert(
            time=datetime.now(),
            ip=ip,
            port=port,
            championId=buffer["championId"],
            champion=buffer["champion"],
            position=buffer["position"],
        ).execute()

        return buffer


class Builds_V1(Resource):
    def get(self, champion, position=""):
        ip = str(request.remote_addr)
        port = str(12345)

        summoner = request.headers.get("Summoner")

        if not summoner:
            summoner = "INCOGNITO"

        logger.info(f"{ip}\t{port}\t{summoner}\t{champion}\t{position}")

        PLAYER.insert(
            time=datetime.now(), ip=ip, port=port, summonername=summoner
        ).execute()

        if position != "":
            build = FINALBUILDS.get_or_none(
                FINALBUILDS.championId == champion,
                FINALBUILDS.position == str(position).lower(),
            )
            if not build:
                build = FINALBUILDS.get_or_none(
                    FINALBUILDS.championId == champion, FINALBUILDS.position == ""
                )
        else:
            build = FINALBUILDS.get_or_none(
                FINALBUILDS.championId == champion, FINALBUILDS.position == ""
            )

        buffer = {}
        buffer["championId"] = build.championId
        buffer["runes"] = build.runes
        buffer["summ"] = build.summ
        buffer["item"] = build.item
        buffer["start_item"] = build.start_item
        buffer["item_build"] = build.item_build
        buffer["skill_order"] = build.skill_order
        buffer["position"] = build.position
        buffer["boots"] = build.boots
        buffer["champion"] = CHAMPIONS.get(CHAMPIONS.key == build.championId).champion
        buffer["champ_winrate"] = build.champ_winrate
        buffer["champ_pickrate"] = build.champ_pickrate

        CONNECTION.insert(
            time=datetime.now(),
            ip=ip,
            port=port,
            championId=buffer["championId"],
            champion=buffer["champion"],
            position=buffer["position"],
        ).execute()

        return buffer


class Version(Resource):
    def get(self):
        ip = str(request.remote_addr)
        port = str(12345)

        logger.info(f"{ip}\t{port}\tVERSION_CHECK")
        
        return version.version


api.add_resource(Builds, "/builds/<champion>/<position>", "/builds/<champion>")
api.add_resource(Builds_V1, "/builds_v1/<champion>/<position>", "/builds_v1/<champion>")
api.add_resource(Version, "/version")
