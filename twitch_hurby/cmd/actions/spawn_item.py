from twitch_hurby.cmd.abstract_command import AbstractCommand


class SpawnItemCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data)
