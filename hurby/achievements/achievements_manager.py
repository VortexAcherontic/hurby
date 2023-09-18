from achievements.achievement import Achievement
from utils import json_loader, logger
from utils.const import Const as CONST

absolute_file = CONST.DIR_CONF_ABSOLUTE + "/" + CONST.FILE_ACHIEVEMENTS
json_data = json_loader.load_json(absolute_file)
achieve_response: str = json_data["achieve_response"]


class AchievementManager:
    def __init__(self, hurby):
        self.achievements = {}
        self.hurby = hurby
        for a in json_data["achievements"]:
            if a not in self.achievements:
                self.achievements[a] = self.__build_achievement(a, json_data["achievements"][a])
            else:
                logger.log(logger.WARN, "Duplicate achievement id: " + a + " omit additional occurrences")
        logger.log(logger.INFO, str(len(self.achievements)) + " achievements loaded")

    def __build_achievement(self, achievement_id: str, achievement_json: dict):
        return Achievement(achievement_id, achievement_json)

    def chat_achievement(self, hurby, achievement_id: str, scope_object):
        title = self.achievements[achievement_id]["title"]
        condition = self.achievements[achievement_id]["condition"]
        reward = self.achievements[achievement_id]["reward_credits"]
        response = achieve_response \
            .replace("$user", scope_object.twitchid) \
            .replace("$title", title) \
            .replace("$condition", condition) \
            .replace("$reward", reward) \
            .replace("$streamer", hurby.twitch_receiver.twitch_conf.streamer)
        hurby.twitch_receiver.twitch_listener.send_message(response)

    def check(self, hook, scope, achieve_type, scope_object, trigger_reference):
        for a in self.achievements:
            if a.validate(hook, scope, achieve_type, scope_object, trigger_reference):
                a.achieve(scope_object)
                self.chat_achievement(self.hurby, a.id, scope_object)
