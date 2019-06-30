import uuid

from utils import hurby_utils, logger


class Character:
    ID_TYPE_TWITCH = "twitchid"
    ID_TYPE_DISCORD = "discordid"
    ID_TYPE_YOUTUBE = "youtubeid"
    ID_TYPE_TWITTER = "twitterid"
    PERM_EVE = "everybody"
    PERM_MOD = "moderator"
    PERM_ADM = "administrator"

    def __init__(self):
        self.credits = None
        self.endurance = None
        self.endurance_max = None
        self.inventory = [None]
        self.mails = None
        self.twitchid = None
        self.twitterid = None
        self.discordid = None
        self.youtubeid = None
        self.name = None
        self.can_do_mini_game = True
        self.uuid = None
        self.perm = Character.PERM_EVE

    def init_default_character(self, name):
        logger.log(logger.INFO, "New default character: " + name)
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

    def set_twitch_id(self, id):
        self.twitchid = id

    def set_discord_id(self, id):
        self.discordid = id

    def add_mail(self, mail):
        if len(self.mails) == 0:
            self.mails = [None]
            self.mails[0] = mail
        else:
            if not self.mail_exists(mail):
                hurby_utils.append_element_to_array(self.mails, mail)

    def mail_exists(self, mail):
        if len(self.mails) > 0:
            for i in range(0, len(self.mails)):
                if self.mails[0] == mail:
                    return True
            return False
        return False

    def parse_json(self, json):
        pass

    def convert_to_json(self):
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
