import re
import time

from character.user_id_types import UserIDType
from twitch_hurby.irc import irc_chat_extractor
from twitch_hurby.irc.threads.hurby_thread import HurbyThread
from utils import logger
from utils.const import CONST


class ReadChat (HurbyThread):
    def __init__(self, irc_connector, tick, twitch_receiver):
        HurbyThread.__init__(self)
        self.irc_connector = irc_connector
        self.tick = tick
        self.receiver = twitch_receiver

    def run(self):
        logger.log(logger.INFO, "Running ReadChat")
        while CONST.RUNNING:
            time.sleep(self.tick)
            self.read_chat()
        logger.log(logger.INFO, "Stopped reading chat")

    def stop(self):
        self._stop_event.set()

    def read_chat(self):
        con = self.irc_connector.connection
        data = con.recv(1024).decode('UTF-8')
        # logger.log(logger.INFO, data)
        data_split = re.split(r"[~\r\n]+", data)
        logger.log(logger.INFO, data_split)
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    self.irc_connector.ping_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = irc_chat_extractor.extract_sender(line[0])
                    self.irc_connector.crawler_thread.crawl_chatters()
                    char = self.irc_connector.hurby.get_char_manager().get_char(sender, UserIDType.TWITCH)
                    message = irc_chat_extractor.extract_message(line)
                    if message.startswith("!"):
                        cmd = irc_chat_extractor.extract_command(message)
                        self.receiver.do_command(cmd, char, self.irc_connector)