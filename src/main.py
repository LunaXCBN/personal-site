"""Websites main file."""
from flask import Flask, render_template
from dotenv import load_dotenv
import platform
import datetime
import requests
import json
import os
import importlib.metadata

load_dotenv()
app = Flask(__name__,
            template_folder="templates",  # Static template folder
            static_folder="static")  # Static file folder


@app.route("/")
def index():
    """Returns the main page of the site."""
    # Calculate age by birthdate
    born = datetime.date(2004, 2, 19)
    today = datetime.date.today()
    age = today.year - born.year - ((today.month,
                                    today.day) < (born.month,
                                                  born.day))

    def steamStatus():
        """
        Function that gets an users online status from the steam web api.

        Returns:
            status: Current status of the user.
            status_color: The color used for the status.
        """
        STEAMAPIKEY = os.getenv("STEAMAPIKEY")
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAMAPIKEY}&format=json&steamids=76561198148554560"
        headers = {"content-type": "application/json"}
        response = requests.get(url, headers=headers)

        json_data = json.loads(response.text)
        status_code = json_data["response"]["players"][0]["personastate"]
        try:
            currently_playing = json_data["response"]["players"][0]["gameextrainfo"]
        except KeyError:
            currently_playing = "None"

        status = 0
        status_color = 0

        # Dictionaries for different personastate codes.
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

        # If loop to check if the user is playing a game.
        if currently_playing == "None":
            status = status_dict.get(status_code, "Unknown")
            status_color = status_color_dict.get(status_code, "#FFF")
        else:
            status = f"Playing: {currently_playing}"
            status_color = "#8fb93b"

        return status, status_color

    def lastfmTracks():
        """
        Function that gets currently playing track from LastFM.

        Returns:
            artist: Track artist
            song: Track name
            cover: Track cover art
        """
        LASTFMAPIKEY = os.getenv("LASTFMAPIKEY")
        url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=aleksivibes&api_key={LASTFMAPIKEY}&format=json&limit=1"
        headers = {"content-type": "application/json"}
        response = requests.get(url, headers=headers)

        json_data = json.loads(response.text)

        artist = json_data["recenttracks"]["track"][0]["artist"]["#text"]
        song = json_data["recenttracks"]["track"][0]["name"]
        cover = json_data["recenttracks"]["track"][0]["image"][3]["#text"]

        return artist, song, cover

    status, status_color = steamStatus()
    artist, song, cover = lastfmTracks()
    flask_version = importlib.metadata.version('flask')
    python_version = platform.python_version()

    return render_template('index.html',
                           bday=age,
                           status=status,
                           status_color=status_color,
                           flask_version=flask_version,
                           python_version=python_version,
                           artist=artist,
                           song=song,
                           cover=cover)


# Start the website
if __name__ == "__main__":
    app.run(debug=True)
