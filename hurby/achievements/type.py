from enum import Enum


class Type(Enum):
    MESSAGE_COUNT = "msg_count"
    SUBSCRIBE_COUNT_IN_ROW = "sub_count_row"
    SUBSCRIBE_GIFT_COUNT = "sub_gift"
    CREDITS_GIFT = "gift_credits"
    CREDITS_TOTAL = "total_credits"
    CREDITS_SPEND = "spend_credits"
    WATCH_TIME = "watch_time"
