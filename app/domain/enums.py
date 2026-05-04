from enum import Enum


class MarketType(str, Enum):
    OVER_0_5_HT = "OVER_0_5_HT"
    OVER_1_5_HT = "OVER_1_5_HT"
    OVER_0_5_FT = "OVER_0_5_FT"
    OVER_1_5_FT = "OVER_1_5_FT"
    OVER_2_5_FT = "OVER_2_5_FT"
    NEXT_GOAL = "NEXT_GOAL"


class PeriodType(str, Enum):
    FIRST_HALF = "FIRST_HALF"
    SECOND_HALF = "SECOND_HALF"
    FULL_TIME = "FULL_TIME"


class MethodStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    TESTING = "TESTING"
    ARCHIVED = "ARCHIVED"
