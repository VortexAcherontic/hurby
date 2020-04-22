import random
import smtplib
import time
from datetime import datetime
from math import ceil

from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from utils import logger


class BugReportCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.hurby = hurby
        self.answers = json_data["answers"]
        self.to_many_requests = json_data["to_many_requests"]
        self.report_mail = json_data["report_mail"]
        self.sender_mail = json_data["sender_mail"]
        self.time_between_reports_in_min = json_data["time_between_reports_in_min"]
        self.smpt_host = json_data["smpt_host"]
        self.smpt_port = json_data["smpt_port"]
        self.sender_password = json_data["sender_password"]
        self.last_report_times = {}

    def do_command(self, params: list, character: Character):
        if character is not None:
            irc = self.hurby.twitch_receiver.twitch_listener
            cur_answer = ""
            if self._can_submit_issue(character):
                cur_answer = self.answers[random.randint(0, len(self.answers) - 1)]
                cur_answer = cur_answer.replace("$user", character.twitchid)
                self._send_mail(params)
                fmt = '%Y-%m-%d %H:%M:%S.%f'
                self.last_report_times[character.twitchid] = datetime.strptime(str(datetime.now()), fmt)
            irc.send_message(cur_answer)

    def _can_submit_issue(self, character: Character):
        fmt = '%Y-%m-%d %H:%M:%S.%f'
        if character.twitchid in self.last_report_times:
            report_time = datetime.now()
            d1 = datetime.strptime(str(self.last_report_times[character.twitchid]), fmt)
            d2 = datetime.strptime(str(report_time), fmt)
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            time_past = ceil(((d2_ts - d1_ts) / 60))
            return time_past >= self.time_between_reports_in_min
        else:
            return True

    def _send_mail(self, params: list):
        msg = ""
        for p in params:
            msg += p + "\n"
        server = smtplib.SMTP_SSL(self.smpt_host, self.smpt_port)
        server.login(self.sender_mail, self.sender_password)
        body = self._build_mail(self.sender_mail, self.report_mail, "Hurby Bug Report", msg)
        try:
            server.sendmail(self.sender_mail, [self.report_mail], body)
            logger.log(logger.INFO, "Bug report Mail send")
        except Exception as e:
            logger.log(logger.WARN, ["Bug report Mail could not be send", str(e)])
        server.quit()

    def _build_mail(self, sender, receiver, subject, message):
        return '\r\n'.join(["To: %s" % receiver,
                            "From: %s" % sender,
                            "Subject: %s" % subject,
                            "MIME-Version: 1.0",
                            "Content-Type: text/plain; charset=utf-8; format=flowed",
                            "Content-Transfer-Encoding: 7bit",
                            "Content-Language: en-GB",
                            "",
                            message])
