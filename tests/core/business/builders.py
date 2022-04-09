from datetime import date

from app.core.utils.constants import AssetType, EventType, CurrencyType
from app.core.business.trade_notes.models import (
    BaseTradeNote,
    BaseTradeNoteItem
)
from app.core.business.subscriptions.models import BaseSubscription


class SubscriptionBuilder:

    def __init__(self) -> None:
        self._subscription = BaseSubscription(
            broker="xpto broker",
            event_date=date.today(),
            effective_event_date=date.today(),
            asset_code="xpto11",
            asset_type=AssetType.BRL_STOCKS,
            asset_derived_code="xpto12",
            quantity=1,
            unit_value=1,
            costs=0.1,
            currency=CurrencyType.BRL,
            note="subscription note"
        )

    def build(self):
        return self._subscription

    def with_broker(self, broker):
        self._subscription.broker = broker
        return self

    def with_event_date(self, event_date):
        self._subscription.event_date = event_date
        return self

    def with_effective_event_date(self, effective_event_date):
        self._subscription.effective_event_date = effective_event_date
        return self

    def with_asset_code(self, asset_code):
        self._subscription.asset_code = asset_code
        return self

    def with_asset_type(self, asset_type):
        self._subscription.asset_type = asset_type
        return self

    def with_asset_derived_code(self, asset_derived_code):
        self._subscription.asset_derived_code = asset_derived_code
        return self

    def with_quantity(self, quantity):
        self._subscription.quantity = quantity
        return self

    def with_unit_value(self, unit_value):
        self._subscription.unit_value = unit_value
        return self

    def with_costs(self, costs):
        self._subscription.costs = costs
        return self

    def with_currency(self, currency):
        self._subscription.currency = currency
        return self

    def with_note(self, note):
        self._subscription.note = note
        return self

    @staticmethod
    def ensure_builder():
        setattr(BaseSubscription, "builder", staticmethod(
            lambda: SubscriptionBuilder()))


class TradeNoteBuilder:

    def __init__(self) -> None:
        self._trade_note = BaseTradeNote(
            note_id="abc123",
            broker="xpto broker",
            trade_date=date.today(),
            liquidate_date=date.today(),
            total_amount=1.1,
            currency=CurrencyType.BRL,
            note_items=[TradeNoteBuilder.TradeNoteItemBuilder().build()]
        )

    def build(self):
        return self._trade_note

    def with_note_id(self, note_id):
        self._trade_note.note_id = note_id
        return self

    def with_broker(self, broker):
        self._trade_note.broker = broker
        return self

    def with_trade_date(self, trade_date):
        self._trade_note.trade_date = trade_date
        return self

    def with_liquidate_date(self, liquidate_date):
        self._trade_note.liquidate_date = liquidate_date
        return self

    def with_total_amount(self, total_amount):
        self._trade_note.total_amount = total_amount
        return self

    def with_currency(self, currency):
        self._trade_note.currency = currency
        return self

    def with_note_items(self, note_items):
        self._trade_note.note_items = note_items
        return self

    @staticmethod
    def ensure_builder():
        setattr(BaseTradeNote, "builder", staticmethod(
            lambda: TradeNoteBuilder()))

    class TradeNoteItemBuilder:

        def __init__(self) -> None:
            self._item = BaseTradeNoteItem(
                asset_code="xpto11",
                asset_type=AssetType.BRL_STOCKS,
                event_type=EventType.BUY,
                quantity=1,
                unit_value=1
            )

        def build(self):
            return self._item

        def with_asset_code(self, asset_code):
            self._item.asset_code = asset_code
            return self

        def with_asset_type(self, asset_type):
            self._item.asset_type = asset_type
            return self

        def with_event_type(self, event_type):
            self._item.event_type = event_type
            return self

        def with_quantity(self, quantity):
            self._item.quantity = quantity
            return self

        def with_unit_value(self, unit_value):
            self._item.unit_value = unit_value
            return self

        @staticmethod
        def ensure_builder():
            setattr(BaseTradeNoteItem, "builder", staticmethod(
                lambda: TradeNoteBuilder.TradeNoteItemBuilder()))
