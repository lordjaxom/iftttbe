#!/opt/iftttbe/flask/bin/python

from flask import Flask
from flask_httpauth import HTTPTokenAuth
from openhab import OpenHAB
from pathlib import Path
from typing import Optional

base_dir = Path(__file__).parent

TOKEN = (base_dir / "ifttt-credentials").read_text()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

openhab = OpenHAB(
    base_url = "http://openhab:8080/rest",
    username = (base_dir / "openhab-credentials").read_text(),
    password = ""
)


@auth.verify_token
def verify_token(token: str) -> Optional[str]:
    if token == TOKEN:
        return "ifttt"
    return None


@app.route("/device-action/<device>/<action>")
@auth.login_required
def device_action(device: str, action: str) -> str:
    if device == "Presence-Office":
        if action == "Presence":
            openhab.get_item("Office_Sensor_Presence_State").state = "ON"
        elif action == "Absence":
            openhab.get_item("Office_Sensor_Presence_State").state = "OFF"
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
