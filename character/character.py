import uuid

from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from utils import hurby_utils, logger, json_loader
from utils.const import CONST


class Character:

    def __init__(self):
        self.credits: int = None
        self.endurance: int = None
        self.endurance_max: int = None
        self.inventory: list = None
        self.mails: list[str] = None
        self.twitchid: str = None
        self.twitterid: str = None
        self.discordid: str = None
        self.youtubeid: str = None
        self.name: str = None
        self.can_do_mini_game: bool = True
        self.uuid: str = None
        self.perm: str = PermissionLevels.EVERYBODY
        self.last_seen = None

    def init_default_character(self, name: str, permission_level: PermissionLevels):
        logger.log(logger.INFO, "New character: " + name)
        self.name = name
        self.credits = 100
        self.endurance = 100
        self.endurance_max = 100
        self.inventory = [None]
        self.mails = [None]
        self.twitchid = None
        self.twitterid = None
        self.discordid = None
        self.youtubeid = None
        self.name = None
        self.can_do_mini_game = True
        self.uuid = str(uuid.uuid4())
        self.perm = permission_level.value

    def set_twitch_id(self, user_id):
        self.twitchid = user_id

    def set_discord_id(self, user_id):
        self.discordid = user_id

    def set_twitter_id(self, user_id):
        self.twitterid = user_id

    def add_mail(self, mail):
        if len(self.mails) == 0:
            self.mails = [None]
            self.mails[0] = mail
        else:
            if not self.mail_exists(mail):
                hurby_utils.append_element_to_array(self.mails, mail)

    def mail_exists(self, mail) -> bool:
        if len(self.mails) > 0:
            for i in range(0, len(self.mails)):
                if self.mails[0] == mail:
                    return True
            return False
        return False

    def parse_json(self, json):
        self.uuid = json["uuid"]
        self.name = json["name"]
        self.credits = json["credits"]
        self.endurance = json["endurance_cur"]
        self.endurance_max = json["endurance_max"]
        self.discordid = json["discordid"]
        self.twitchid = json["twitchid"]
        self.youtubeid = json["youtubeid"]
        self.twitterid = json["twitterid"]
        self.mails = json["mail"]
        self.inventory = json["inventory"]
        self.perm = PermissionLevels[json["permission_level"].upper()]

    def convert_to_json(self) -> dict:
        text = {
            "uuid": self.uuid,
            "name": self.name,
            "credits": self.credits,
            "endurance_cur": self.endurance,
            "endurance_max": self.endurance_max,
            "discordid": self.discordid,
            "twitchid": self.twitchid,
            "youtubeid": self.youtubeid,
            "twitterid": self.twitterid,
            "mail": [self.mails],
            "inventory": [self.inventory],
            "permission_level": self.perm
        }
        return text

    def save(self):
        data = self.convert_to_json()
        file = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + str(self.uuid) + ".json"
        json_loader.save_json(file, data)

    def load(self, json_file_name):
        absolute_file = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + json_file_name
        json_data = json_loader.loadJSON(absolute_file)
        self.parse_json(json_data)
