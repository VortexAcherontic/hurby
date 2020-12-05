from character.character import Character
from modules.lottery.lottery_manager import LotteryManager, ParticipateStatus
from twitch_hurby.cmd.abstract_command import AbstractCommand
from utils import hurby_utils, logger


class LotteryCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.lottery_manager: LotteryManager = self.hurby.lottery_manager

    def do_command(self, params: list, character: Character):
        sub_command = self._get_subcommand_by_trigger(params)
        if sub_command["internal_trigger"] == "$lot_apply":
            if self._has_multiple_lotteries():
                if len(params) >= 2:
                    if isinstance(params[1], int):
                        self._respond_on_participate(self._apply_for_lottery(params[1], character))
                    elif isinstance(params[1], str):
                        if self.hurby.botConfig.commands_case_sensitive:
                            if params[1] == "all":
                                pass
                        else:
                            if params[1].lower() == "all".lower():
                                pass
            else:
                self.lottery_manager.try_participate(character, 0)

    def _apply_for_lottery(self, lottery_id, character):
        return self.lottery_manager.try_participate(character, 0)

    def _has_multiple_lotteries(self):
        return self.lottery_manager.get_amount_of_lotteries() > 1

    def _respond_on_participate(self, participate_status):
        message = ""
        if participate_status == ParticipateStatus.SUCCESS:
            message = hurby_utils.get_random_reply(self.lottery_manager.success_participate)
        elif participate_status == ParticipateStatus.IS_FULL:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_lottery_full_response)
        elif participate_status == ParticipateStatus.MAX_TICKETS_REACHED:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_max_tickets_reached)
        elif participate_status == ParticipateStatus.INSUFFICIENT_CREDITS:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_insufficient_credits_response)
        else:
            logger.log(logger.WARN, "Unknown ParticipateStatus: " + participate_status)
        self.irc.send_message(message)
