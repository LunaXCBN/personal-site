import json
import requests

def steamapi():
    api_key = "E88C8F550DFA5B17B4156616A25C6893"
    steam_id = "76561198148554560"
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&format=json&steamids={steam_id}"
    headers = {"content-type": "application/json"}
    response = requests.get(url, headers=headers)

    json_data = json.loads(response.text)
    status = json_data["response"]["players"][0]["personastate"]
    print(status)

steamapi()