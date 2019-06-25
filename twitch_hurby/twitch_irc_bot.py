from python_twitch_irc import TwitchIrc


class TwitchIRCBot(TwitchIrc):
    async def on_connect(self):
        self.join('#zrayentertainment')

    # Override from base class
    async def on_message(self, timestamp, tags, channel, user, message):
        self.message(channel, message)
