import re
import socket
import threading

from twitch_hurby.irc.irc_chat_extractor import IRCChatExtractor
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger


class IRCConnector:
    def __init__(self, username: str, password: str, receiver, tick=1):
        self.host = TwitchConfig.HOST
        self.port = TwitchConfig.PORT
        self.username = username
        self.password = password
        self.connection = None
        self.tick = tick
        self.receiver = receiver
        self.thread = None
        self.channel = None
        self.extractor = IRCChatExtractor

    def connect(self):
        self.connection = socket.socket()
        self.connection.connect((self.host, self.port))
        self.connection.send(bytes('PASS %s\r\n' % self.password, 'UTF-8'))
        self.connection.send(bytes('NICK %s\r\n' % self.username, 'UTF-8'))

    def join_channel(self, channel: str):
        self.connection.send(bytes('JOIN %s\r\n' % channel, 'UTF-8'))

    def start(self, channel: str):
        self.channel = channel
        self.connect()
        self.join_channel(self.channel)
        self.thread = threading.Thread(target=self.loop())
        self.thread.start()

    def loop(self):
        ctc = 0
        while True:
            # time.sleep(self.tick)
            ctc += 1
            self.read_chat()
            # self.send_message("Tick: " + str(ctc))
            # logger.log(logger.INFO, "Tick: " + str(ctc))

    def read_chat(self):
        data = self.connection.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        logger.log(logger.INFO, data_split)
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    self.ping_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = self.extractor.extract_sender(line[0])
                    message = self.extractor.extract_message(line)
                    if message.startswith("!"):
                        self.receiver.do_command(message, None, None, self)
        # self.check_viewers()

    def check_viewers(self):
        self.connection.send(bytes('WHO %s\r\n' % self.channel, 'UTF-8'))

    def send_message(self, msg):
        self.connection.send(bytes('PRIVMSG %s :%s\r\n' % (self.channel, msg), 'UTF-8'))

    def ping_pong(self, msg: str):
        self.connection.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))
