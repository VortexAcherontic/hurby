import requests


def get_twitch_bot_names() -> dict:
    url = "https://raw.githubusercontent.com/tarumes/twitch-ban-list/master/public_ban.json"
    external_json = requests.get(url).json()
    bots = {
        "names": [],
        "ids": []
    }
    for user in external_json:
        if user["reason"] == "bot_account":
            bots["names"].append(user["twitch_name"])
            bots["ids"].append(user["twitch_id"])

    return bots
