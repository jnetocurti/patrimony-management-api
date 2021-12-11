from enum import Enum, auto


class _AutoName(Enum):
    def _generate_next_value_(name, *_):
        return name


class AssetType(str, _AutoName):
    BRL_STOCKS = auto()
    USA_STOCKS = auto()
    BRL_ETF = auto()
    USA_ETF = auto()
    BDR = auto()
    REITS = auto()
    REAL_ESTATE_FUNDS = auto()


class EventType(str, _AutoName):
    BUY = auto()
    SALE = auto()
    SUBSCRIPTION = auto()
    EARNINGS = auto()


class CurrencyType(str, _AutoName):
    BRL = auto()
    USD = auto()
