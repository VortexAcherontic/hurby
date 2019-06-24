from utils import JSONLoader, Logger
from utils.Const import CONST


class Blacklist:
    DIR_CHARACTER = CONST.DIR_APP_DATA_ABSOLUTE + "/characters"

    def __init__(self):
        black_list_json = JSONLoader.loadJSON(Blacklist.DIR_CHARACTER + "/" + CONST.FILE_BLACKLIST)
        self.len_black_list = len(black_list_json["blacklist"])
        self.blacklist = [None] * self.len_black_list
        for i in range(0, self.len_black_list):
            self.blacklist[i] = black_list_json["blacklist"][i]
            Logger.log(Logger.INFO, "Blacklisted: " + self.blacklist[i])

    def is_black_listed(self, user):
        for i in range(0, self.len_black_list):
            if user == self.blacklist[i]:
                return True
        return False
