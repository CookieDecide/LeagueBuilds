from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from models.builds_db import FINALBUILDS
from models.statics_db import CHAMPIONS
import version
from models.log_db import CONNECTION, PLAYER
import logging, os
import ast
from uuid import uuid4

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


def redact_ip(address):
    if not address:
        return "unknown"

    if ":" in address:
        return "[redacted-ipv6]"

    parts = address.split(".")
    if len(parts) == 4:
        return ".".join(parts[:3] + ["0"])

    return "[redacted-ip]"

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
api = Api(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[os.getenv("LEAGUEBUILDS_RATE_LIMIT_DEFAULT", "120 per minute")],
    storage_uri=os.getenv("LEAGUEBUILDS_RATE_LIMIT_STORAGE_URI", "memory://"),
    headers_enabled=True,
)


@app.errorhandler(429)
def handle_ratelimit(_error):
    return {
        "error": "rate_limited",
        "message": "Too many requests, please try again later.",
    }, 429


def start_server():
    host = "127.0.0.1"
    port = 12345
    try:
        from waitress import serve
    except ImportError:
        raise RuntimeError("waitress is required to run the server")

    thread_count = int(os.getenv("LEAGUEBUILDS_SERVER_THREADS", "8"))
    trusted_proxy = os.getenv("LEAGUEBUILDS_TRUSTED_PROXY", "127.0.0.1")
    trusted_proxy_count = int(os.getenv("LEAGUEBUILDS_TRUSTED_PROXY_COUNT", "1"))
    trusted_proxy_headers = {
        "x-forwarded-for",
        "x-forwarded-host",
        "x-forwarded-proto",
        "x-forwarded-port",
        "x-forwarded-by",
    }

    logger.info(
        "Starting production server (waitress) on %s:%s with %s threads",
        host,
        port,
        thread_count,
    )

    serve_kwargs = {
        "host": host,
        "port": port,
        "threads": thread_count,
        "trusted_proxy": trusted_proxy,
        "trusted_proxy_count": trusted_proxy_count,
        "trusted_proxy_headers": trusted_proxy_headers,
    }

    try:
        serve(app, **serve_kwargs)
    except TypeError:
        logger.warning(
            "Installed waitress does not support trusted_proxy options; "
            "falling back to default waitress settings."
        )
        serve(app, host=host, port=port, threads=thread_count)


# Deprecated: Endpoint for v1.0.0, will be removed in future versions. Use /builds_v1 instead.
class Builds(Resource):
    decorators = [limiter.limit(os.getenv("LEAGUEBUILDS_RATE_LIMIT_BUILDS", "60 per minute;10 per second"))]

    def get(self, champion, position=""):
        request_id = uuid4().hex[:8]
        ip = str(request.remote_addr)
        port = str(12345)

        summoner = request.headers.get("Summoner")

        if not summoner:
            summoner = "INCOGNITO"

        logger.info(
            "%s\t%s\t%s\t%s",
            request_id,
            redact_ip(ip),
            champion,
            position,
        )

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
    decorators = [limiter.limit(os.getenv("LEAGUEBUILDS_RATE_LIMIT_BUILDS_V1", "60 per minute;10 per second"))]

    def get(self, champion, position=""):
        request_id = uuid4().hex[:8]
        ip = str(request.remote_addr)
        port = str(12345)

        summoner = request.headers.get("Summoner")

        if not summoner:
            summoner = "INCOGNITO"

        logger.info(
            "%s\t%s\t%s\t%s",
            request_id,
            redact_ip(ip),
            champion,
            position,
        )

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
    decorators = [limiter.limit(os.getenv("LEAGUEBUILDS_RATE_LIMIT_VERSION", "600 per minute"))]

    def get(self):
        ip = str(request.remote_addr)
        port = str(12345)

        logger.info(f"{ip}\t{port}\tVERSION_CHECK")
        
        return version.version


api.add_resource(Builds, "/builds/<champion>/<position>", "/builds/<champion>")
api.add_resource(Builds_V1, "/builds_v1/<champion>/<position>", "/builds_v1/<champion>")
api.add_resource(Version, "/version")
