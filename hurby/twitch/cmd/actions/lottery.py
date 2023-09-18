from character.character import Character
from modules.lottery import lottery_manager
from modules.lottery.lottery_manager import LotteryManager, ParticipateStatus
from twitch.cmd.abstract_command import AbstractCommand
from utils import logger, hurby_utils


class LotteryCommand(AbstractCommand):
    def __init__(self, json_data, hurby):
        AbstractCommand.__init__(self, json_data, hurby)
        self.lottery_manager: LotteryManager = self.hurby.lottery_manager

    def do_command(self, params: list, character: Character):
        sub_command = self._get_subcommand_by_trigger(params)
        if sub_command["internal_trigger"] == "$lot_apply":
            if self._has_multiple_active_lotteries():
                if len(params) >= 2:
                    if self._valid_number(params[1]):
                        self._respond_on_participate(self._apply_for_lottery(params[1], character), character.twitchid)
                    elif self._valid_all(params[1]):
                        lottery_id = 0
                        success = 0
                        while lottery_id <= self.lottery_manager.get_amount_of_lotteries():
                            if self._apply_for_lottery(lottery_id, character) == ParticipateStatus.SUCCESS:
                                success += 1
                            lottery_id += 1
            else:
                active_lottery = self.lottery_manager.get_first_active_lottery()
                self._respond_on_participate(self._apply_for_lottery(active_lottery.lottery_id, character),
                                             character.twitchid)
        elif sub_command["internal_trigger"] == "$lot_start":
            if self._has_multiple_inactive_lotteries():
                if self._valid_number(params[1]):
                    self._start_lottery(params[1])
            else:
                inactive_lottery = self.lottery_manager.get_first_inactive_lottery()
                self._start_lottery(inactive_lottery.lottery_id)
        elif sub_command["internal_trigger"] == "$lot_list":
            active_lotteries_titles = self.lottery_manager.get_active_lottery_names()
            self._respond_on_list_active_lotteries(active_lotteries_titles)
        elif sub_command["internal_trigger"] == "$lot_draw":
            if self._has_multiple_active_lotteries():
                if self._valid_number(params[1]):
                    self._draw_price(self.lottery_manager.get_lottery(params[1]))
            else:
                self._draw_price(self.lottery_manager.get_first_active_lottery())
        elif sub_command["internal_trigger"] == "$lot_end":
            lottery_title = ""
            if self._has_multiple_active_lotteries():
                if self._valid_number(params[1]):
                    self.lottery_manager.end_lottery(params[1])
                    lottery_title = self.lottery_manager.get_lottery(params[1]).lottery_title
            else:
                lottery = self.lottery_manager.get_first_active_lottery()
                lottery_title = lottery.lottery_title
                self.lottery_manager.end_lottery(lottery.lottery_id)
            message = hurby_utils.get_random_reply(self.lottery_manager.lottery_ended_response)
            message = message.replace("$lottery_title", lottery_title)
            self.irc.send_message(message)

    def _draw_price(self, lottery):
        price = lottery.draw_price()
        if price is not None:
            winner_uuid = lottery.draw_winner()
            winner_name = self.hurby.char_manager.get_character_by_uuid(winner_uuid).twitchid
            self._respond_on_winner(price, winner_name)
            lottery_manager.write_lottery_winner(lottery.lottery_title, price, winner_name)
        else:
            self._respond_on_no_prices()

    def _respond_on_winner(self, price, winner_name):
        message = ""
        if self.lottery_manager.expose_winner:
            if self.lottery_manager.expose_won_price_title:
                message = hurby_utils.get_random_reply(
                    self.lottery_manager.winner_drawn_response_expose_winner_and_price_title)
            else:
                message = hurby_utils.get_random_reply(self.lottery_manager.winner_drawn_response_expose_winner)
        elif self.lottery_manager.expose_won_price_title:
            message = hurby_utils.get_random_reply(self.lottery_manager.winner_drawn_response_expose_price_title)
        else:
            message = hurby_utils.get_random_reply(self.lottery_manager.winner_drawn_response_no_expose)
        message = message.replace("$user", winner_name)
        message = message.replace("$price_title", price.price_title)
        self.irc.send_message(message)

    def _respond_on_no_prices(self):
        message = hurby_utils.get_random_reply(self.lottery_manager.error_no_price_left)
        self.irc.send_message(message)

    def _apply_for_lottery(self, lottery_id, character):
        return self.lottery_manager.try_participate(character, lottery_id)

    def _has_multiple_lotteries(self):
        return self.lottery_manager.get_amount_of_lotteries() > 1

    def _has_multiple_active_lotteries(self):
        return self.lottery_manager.get_amount_of_active_lotteries() > 1

    def _has_multiple_inactive_lotteries(self):
        return self.lottery_manager.get_amount_of_inactive_lotteries() > 1

    def _respond_on_list_active_lotteries(self, lottery_titles):
        message = ""
        if self.lottery_manager.has_active_lotteries():
            message_header = hurby_utils.get_random_reply(self.lottery_manager.running_lotteries_response_header)
            message_item = hurby_utils.get_random_reply(self.lottery_manager.running_lotteries_response_item)
            message = message_header + " "
            for title in lottery_titles:
                tmp_item = message_item
                message += tmp_item.replace("$lottery_title", title)
        else:
            message = hurby_utils.get_random_reply(self.lottery_manager.no_lotteries_response)
        self.irc.send_message(message)

    def _respond_on_participate(self, participate_status, user_name):
        message = ""
        if participate_status == ParticipateStatus.SUCCESS:
            message = hurby_utils.get_random_reply(self.lottery_manager.success_participate)
        elif participate_status == ParticipateStatus.IS_FULL:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_lottery_full_response)
        elif participate_status == ParticipateStatus.MAX_TICKETS_REACHED:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_max_tickets_reached)
        elif participate_status == ParticipateStatus.INSUFFICIENT_CREDITS:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_insufficient_credits_response)
        elif participate_status == ParticipateStatus.LOTTERY_INACTIVE:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_lottery_is_inactive)
        elif participate_status == ParticipateStatus.NO_ACTIVE_LOTTERY:
            message = hurby_utils.get_random_reply(self.lottery_manager.no_lotteries_response)
        elif participate_status == ParticipateStatus.NOT_ENOUGH_WATCH_TIME:
            message = hurby_utils.get_random_reply(self.lottery_manager.error_insufficient_watchtime_response)
        else:
            logger.log(logger.WARN, "Unknown ParticipateStatus: " + participate_status)

        message = message.replace("$user", user_name)
        message = message.replace("$ticket_price", str(self.lottery_manager.ticket_price))
        message = message.replace("$watchtime", str(self.lottery_manager.min_watch_time_in_mins))
        self.irc.send_message(message)

    def _start_lottery(self, lottery_id):
        self.lottery_manager.start_lottery(lottery_id)
        lottery_name = self.lottery_manager.get_lottery_name(lottery_id)
        self._respond_on_lottery_start(lottery_name)

    def _respond_on_lottery_start(self, lottery_name):
        message = hurby_utils.get_random_reply(self.lottery_manager.lottery_started_response)
        message = message.replace("$lottery_title", lottery_name)
        message = message.replace("$command_trigger", self.trigger[0])
        sub_trigger = ""
        for sub in self.sub_commands:
            if sub["internal_trigger"] == "$lot_apply":
                sub_trigger = sub["trigger"][0]
        message = message.replace("$command_sub_trigger_lot_apply", sub_trigger)
        if self._has_multiple_active_lotteries():
            lottery_id_string = ""
            for lot_id in self.lottery_manager.get_active_lottery_ids():
                lottery_id_string = str(lot_id) + "|"
            message = message.replace("$command_sub_trigger_lot_apply", lottery_id_string)
        else:
            message = message.replace("$lottery_id", "")
        self.irc.send_message(message)

    def _valid_number(self, input_value):
        if isinstance(input_value, int):
            return input_value >= 0
        return False

    def _valid_all(self, input_value):
        if isinstance(input_value, str):
            if self.hurby.botConfig.commands_case_sensitive:
                return input_value == "all"
            else:
                return input_value.lower() == "all".lower()
