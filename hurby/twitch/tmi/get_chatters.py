import requests

from hurby.twitch.irc.threads.crawler.chatter_types import ChatterType


def get_chatters_for_channels(channels: list) -> dict:
    dict_chatters = {
        ChatterType.BROADCASTER: [],
        ChatterType.VIP: [],
        ChatterType.MODERATOR: [],
        ChatterType.STAFF: [],
        ChatterType.ADMINS: [],
        ChatterType.GLOBAL_MODERATORS: [],
        ChatterType.VIEWER: []
    }

    for ch in channels:
        url = "https://tmi.twitch.tv/group/user/" + ch + "/chatters"
        r = requests.get(url)
        chatters_json = r.json()
        dict_chatters[ChatterType.BROADCASTER] += chatters_json["chatters"]["broadcaster"]
        dict_chatters[ChatterType.VIP] += chatters_json["chatters"]["vips"]
        dict_chatters[ChatterType.MODERATOR] += chatters_json["chatters"]["moderators"]
        dict_chatters[ChatterType.STAFF] += chatters_json["chatters"]["staff"]
        dict_chatters[ChatterType.ADMINS] += chatters_json["chatters"]["admins"]
        dict_chatters[ChatterType.GLOBAL_MODERATORS] += chatters_json["chatters"]["global_mods"]
        dict_chatters[ChatterType.VIEWER] += chatters_json["chatters"]["viewers"]
    return dict_chatters


def get_all_chatters_as_list(channels: list) -> list:
    all_chatters = []
    chatter_dict = get_chatters_for_channels(channels)
    for chatter_type in chatter_dict:
        chatters_for_type = chatter_dict[chatter_type]
        all_chatters += chatters_for_type
    return all_chatters
