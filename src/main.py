"""Websites main file."""
from flask import Flask, render_template
import datetime
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__,
            template_folder="templates",
            static_folder="static")


@app.route("/")
def index():
    """Returns the main page of the site."""
    born = datetime.date(2004, 2, 19)
    today = datetime.date.today()
    age = today.year - born.year - ((today.month,
                                    today.day) < (born.month,
                                                  born.day))

    def steamStatus():
        STEAMAPIKEY = os.getenv("STEAMAPIKEY")
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAMAPIKEY}&format=json&steamids=76561198148554560"
        headers = {"content-type": "application/json"}
        response = requests.get(url, headers=headers)

        json_data = json.loads(response.text)
        status_code = json_data["response"]["players"][0]["personastate"]
        try:
            currently_playing = json_data["response"]["players"][0]["gameextrainfo"]
            print(currently_playing)
        except KeyError:
            currently_playing = "None"
            print(currently_playing)

        status_dict = {0: "Offline",
                       1: "Online",
                       2: "Busy",
                       3: "Away",
                       4: "Snooze"}
        status_color_dict = {0: "#6a6a6a",
                             1: "#53a4c4",
                             2: "#ff1a1a",
                             3: "#ffff00",
                             4: "#ffff00"}

        if currently_playing == "None":
            status = status_dict.get(status_code, "Unknown")
            status_color = status_color_dict.get(status_code, "#FFF")
        else:
            status = f"Playing: {currently_playing}"
            status_color = "#8fb93b"

        return status, status_color

    status, status_color = steamStatus()

    return render_template('index.html',
                           bday=age,
                           status=status,
                           status_color=status_color)


if __name__ == "__main__":
    app.run(debug=True)
