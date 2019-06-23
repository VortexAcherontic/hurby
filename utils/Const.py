import os


class _Const:
    USER_HOME = os.getenv("HOME")

    DIR_APP_DATA = ".z-ray/hurby"
    DIR_CONF = "config"

    FILE_CONF_HURBY = "hurby_conf.json"
    FILE_LOG = "hurby.log"


CONST = _Const()
