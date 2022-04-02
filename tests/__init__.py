from tests.core.business.builders import TradeNoteBuilder

from app.core.business.trade_notes.models import (
    BaseTradeNote,
    BaseTradeNoteItem
)


def ensure_builders():
    setattr(BaseTradeNote, "builder", staticmethod(lambda: TradeNoteBuilder()))
    setattr(BaseTradeNoteItem, "builder", staticmethod(
        lambda: TradeNoteBuilder.TradeNoteItemBuilder()))
