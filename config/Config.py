import json

from utils import Const


class Config:
    def load_config(self):
        file = Const.CONST.USER_HOME + "/" + Const.CONST.DIR_APP_DATA + "/" + Const.CONST.DIR_CONF + "/" + \
               Const.CONST.FILE_CONF_HURBY

        with open(file) as f:
            d = json.load(f)
            f.close()
            print("Load config from: " + file)
            print(d)