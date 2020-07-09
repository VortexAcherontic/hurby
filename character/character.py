import time
import uuid
from datetime import datetime
from math import ceil

from character.equipment import PlayerEquipment
from character.exceptions.insufficient_credits_exception import InsufficientCreditsException
from character.exceptions.less_than_zero_exception import LessThanZeroException
from character.inventory import PlayerInventory
from character.user_id_types import UserIDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels
from utils import hurby_utils, logger, json_loader
from utils.const import CONST


def _fix_array_ception(array):
    layers_found = 0
    tmp_array = array
    while isinstance(tmp_array, list):
        layers_found += 1
        tmp_array = tmp_array[0]
    logger.log(logger.DEV, "Found: " + str(layers_found) + " layers in array")
    for i in range(0, layers_found - 1):
        array = array[0]
        logger.log(logger.DEV, "Cleaned to: " + str(array))
    return array


class Character:

    def __init__(self, hurby):
        self._credits: int = 0
        self.endurance: int = 0
        self.endurance_max: int = 0
        self.mails: list[str] = [None]
        self.twitchid: str = ""
        self.twitterid: str = ""
        self.discordid: str = ""
        self.youtubeid: str = ""
        self.can_do_mini_game: bool = True
        self.uuid: str = ""
        self.perm = PermissionLevels.EVERYBODY
        self.last_seen = None
        self.is_supporter = False
        self.equipment: PlayerEquipment = PlayerEquipment({}, self.uuid, None)
        self.inventory: PlayerInventory = PlayerInventory(None, hurby)
        self.first_seen = datetime.now()
        self.watchtime_min = 0
        self.hurby = hurby

    def init_default_character(self, user_id: str, permission_level: PermissionLevels, user_id_type: UserIDType):
        logger.log(logger.INFO, "New character: " + user_id)
        self.uuid = str(uuid.uuid4())
        self._credits = 100
        self.endurance = 100
        self.endurance_max = 100
        self.mails = [None]
        self.twitchid = None
        self.twitterid = None
        self.discordid = None
        self.youtubeid = None
        self.can_do_mini_game = True
        self.perm = permission_level
        self.is_supporter = False
        self.first_seen = datetime.now()
        if user_id_type == UserIDType.TWITCH:
            self.twitchid = user_id
        self.watchtime_min = 0

    def get_credits(self):
        return self._credits

    def remove_credits(self, cred: int):
        if int(cred) < 0:
            raise LessThanZeroException("The specified value needs to be zero or positive")
        elif self._credits < int(cred):
            raise InsufficientCreditsException("Not enough credits to be removed", self._credits)
        else:
            self._credits -= int(cred)
            self.save()

    def add_credits(self, cred: int):
        if int(cred) < 0:
            raise LessThanZeroException("The specified value needs to be zero or positive")
        else:
            self._credits += int(cred)
            self.save()

    def set_credits(self, cred: int):
        if int(cred) < 0:
            raise LessThanZeroException("The specified value needs to be zero or positive")
        else:
            self._credits = int(cred)
            self.save()

    def set_permission_level(self, level: PermissionLevels):
        self.perm = level

    def set_supporter(self, status: bool):
        self.is_supporter = status

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
        self._credits = json["credits"]
        self.endurance = json["endurance_cur"]
        self.endurance_max = json["endurance_max"]
        self.discordid = json["discordid"]
        self.twitchid = json["twitchid"]
        self.youtubeid = json["youtubeid"]
        self.twitterid = json["twitterid"]
        self.mails = json["mail"]
        self.perm = PermissionLevels[json["permission_level"].upper()]
        self.is_supporter = json["is_supporter"]
        self.mails = _fix_array_ception(self.mails)
        self.inventory = _fix_array_ception(self.inventory)
        if "equipment" in json:
            self.equipment = PlayerEquipment(json["equipment"], self.uuid, self.hurby.item_manager)
        if "inventory" in json:
            self.inventory = PlayerInventory(json["inventory"], self.hurby)
        if "watchtime_min" in json:
            self.watchtime_min = json["watchtime_min"]

    def update_watchtime(self, minutes=1):
        self.watchtime_min += minutes
        logger.log(logger.DEV, "Watchtime of " + self.uuid + "is now " + str(self.watchtime_min) + " min")
        self.save()

    def save(self):
        data = self._convert_to_json()
        file = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + str(self.uuid) + ".json"
        logger.log(logger.DEV, "Saving character: " + self.uuid)
        json_loader.save_json(file, data)

    def load(self, json_file_name):
        absolute_file = CONST.DIR_CHARACTERS_ABSOLUTE + "/" + json_file_name
        json_data = json_loader.load_json(absolute_file)
        self.parse_json(json_data)
        logger.log(logger.INFO, "Loaded character: twitchID: " + self.twitchid)

    def _convert_to_json(self) -> dict:
        text = {
            "uuid": self.uuid,
            "credits": self._credits,
            "endurance_cur": self.endurance,
            "endurance_max": self.endurance_max,
            "discordid": self.discordid,
            "twitchid": self.twitchid,
            "youtubeid": self.youtubeid,
            "twitterid": self.twitterid,
            "mail": self.mails,
            "permission_level": self.perm.value,
            "is_supporter": self.is_supporter,
            "inventory": self.inventory.to_dict(),
            "equipment": self.equipment.to_dict(),
            "watchtime_min": self.watchtime_min
        }
        return text
