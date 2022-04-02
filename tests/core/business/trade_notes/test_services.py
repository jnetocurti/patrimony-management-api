from datetime import date
from unittest import mock

import pytest
from bson import ObjectId

from app.core.utils.constants import AssetType, EventType, CurrencyType
from app.core.business.events.models import EventDoc
from app.core.business.trade_notes.models import (
    BaseTradeNote,
    BaseTradeNoteItem
)
from app.core.business.trade_notes.services import TradeNoteService


class TestTradeNoteServiceCreate:

    @pytest.mark.asyncio
    async def test_create(self, async_client):

        payload = BaseTradeNote.builder()\
            .with_note_id("987cba")\
            .with_broker("Avenue")\
            .with_trade_date(date(2022, 4, 8))\
            .with_liquidate_date(date(2022, 4, 11))\
            .with_currency(CurrencyType.USD)\
            .with_total_amount(99).build()

        trade_note = await TradeNoteService().create(payload)

        assert trade_note.id is not None
        assert trade_note.broker == payload.broker
        assert trade_note.trade_date == payload.trade_date
        assert trade_note.liquidate_date == payload.liquidate_date
        assert trade_note.currency == payload.currency
        assert trade_note.total_amount == payload.total_amount

    @pytest.mark.asyncio
    async def test_create_items(self, async_client):

        payload = BaseTradeNote.builder()\
            .with_total_amount(1000)\
            .with_note_items([
                BaseTradeNoteItem.builder()
                .with_asset_code("SDIV")
                .with_asset_type(AssetType.USA_ETF)
                .with_event_type(EventType.BUY)
                .with_quantity(4)
                .with_unit_value(100)
                .build(),
                BaseTradeNoteItem.builder()
                .with_asset_code("VPN")
                .with_asset_type(AssetType.USA_ETF)
                .with_event_type(EventType.BUY)
                .with_quantity(6)
                .with_unit_value(100)
                .build()
            ]).build()

        trade_note = await TradeNoteService().create(payload)
        item_one, item_two = trade_note.note_items

        assert item_one.asset_code == payload.note_items[0].asset_code
        assert item_one.asset_type == payload.note_items[0].asset_type
        assert item_one.event_type == payload.note_items[0].event_type
        assert item_one.quantity == payload.note_items[0].quantity
        assert item_one.unit_value == payload.note_items[0].unit_value

        assert item_two.asset_code == payload.note_items[1].asset_code
        assert item_two.asset_type == payload.note_items[1].asset_type
        assert item_two.event_type == payload.note_items[1].event_type
        assert item_two.quantity == payload.note_items[1].quantity
        assert item_two.unit_value == payload.note_items[1].unit_value

    @pytest.mark.asyncio
    async def test_create_calculate_costs(self, async_client):

        payload = BaseTradeNote.builder()\
            .with_total_amount(1000.78)\
            .with_note_items([
                BaseTradeNoteItem.builder()
                .with_quantity(3)
                .with_unit_value(100)
                .build(),
                BaseTradeNoteItem.builder()
                .with_quantity(2)
                .with_unit_value(100)
                .build(),
                BaseTradeNoteItem.builder()
                .with_quantity(5)
                .with_unit_value(100)
                .build()
            ]).build()

        trade_note = await TradeNoteService().create(payload)
        item_one, item_two, item_three = trade_note.note_items

        assert item_one.costs == 0.234
        assert item_two.costs == 0.156
        assert item_three.costs == 0.39

        assert sum([
            sum([item_one.costs, (item_one.unit_value * item_one.quantity)]),
            sum([item_two.costs, (item_two.unit_value * item_two.quantity)]),
            sum([item_three.costs, (item_three.unit_value * item_three.quantity)])  # noqa
        ]) == payload.total_amount


class TestTradeNoteServiceUpdate:

    @pytest.mark.asyncio
    async def test_update(self, async_client):

        payload = BaseTradeNote.builder()\
            .with_note_id("987cba")\
            .with_broker("Avenue")\
            .with_trade_date(date(2022, 4, 8))\
            .with_liquidate_date(date(2022, 4, 11))\
            .with_currency(CurrencyType.USD)\
            .with_total_amount(99).build()

        trade_note = await TradeNoteService().update(
            "624b4f0e2b746ffa4848da79", payload
        )

        assert trade_note.id == "624b4f0e2b746ffa4848da79"
        assert trade_note.broker == payload.broker
        assert trade_note.trade_date == payload.trade_date
        assert trade_note.liquidate_date == payload.liquidate_date
        assert trade_note.currency == payload.currency
        assert trade_note.total_amount == payload.total_amount

    @pytest.mark.asyncio
    @mock.patch.object(EventDoc, "delete_many")
    async def test_update_items(self, delete_many, async_client):

        payload = BaseTradeNote.builder()\
            .with_total_amount(1000)\
            .with_note_items([
                BaseTradeNoteItem.builder()
                .with_asset_code("SDIV")
                .with_asset_type(AssetType.USA_ETF)
                .with_event_type(EventType.BUY)
                .with_quantity(4)
                .with_unit_value(100)
                .build(),
                BaseTradeNoteItem.builder()
                .with_asset_code("VPN")
                .with_asset_type(AssetType.USA_ETF)
                .with_event_type(EventType.BUY)
                .with_quantity(6)
                .with_unit_value(100)
                .build()
            ]).build()

        trade_note = await TradeNoteService().update(
            "624b4f0e2b746ffa4848da79", payload
        )

        item_one, item_two = trade_note.note_items

        assert trade_note.id == "624b4f0e2b746ffa4848da79"
        assert item_one.asset_code == payload.note_items[0].asset_code
        assert item_one.asset_type == payload.note_items[0].asset_type
        assert item_one.event_type == payload.note_items[0].event_type
        assert item_one.quantity == payload.note_items[0].quantity
        assert item_one.unit_value == payload.note_items[0].unit_value

        assert item_two.asset_code == payload.note_items[1].asset_code
        assert item_two.asset_type == payload.note_items[1].asset_type
        assert item_two.event_type == payload.note_items[1].event_type
        assert item_two.quantity == payload.note_items[1].quantity
        assert item_two.unit_value == payload.note_items[1].unit_value

        delete_many.assert_awaited_once_with({
            '_id': {
                '$in': [
                    ObjectId('624b4f0e2b746ffa4848da77'),
                    ObjectId('624b4f0e2b746ffa4848da78')
                ]
            }
        })

    @pytest.mark.asyncio
    async def test_update_calculate_costs(self, async_client):

        payload = BaseTradeNote.builder()\
            .with_total_amount(1000.78)\
            .with_note_items([
                BaseTradeNoteItem.builder()
                .with_quantity(3)
                .with_unit_value(100)
                .build(),
                BaseTradeNoteItem.builder()
                .with_quantity(2)
                .with_unit_value(100)
                .build(),
                BaseTradeNoteItem.builder()
                .with_quantity(5)
                .with_unit_value(100)
                .build()
            ]).build()

        trade_note = await TradeNoteService().update(
            "624b4f0e2b746ffa4848da79", payload
        )

        item_one, item_two, item_three = trade_note.note_items

        assert item_one.costs == 0.234
        assert item_two.costs == 0.156
        assert item_three.costs == 0.39
        assert trade_note.id == "624b4f0e2b746ffa4848da79"

        assert sum([
            sum([item_one.costs, (item_one.unit_value * item_one.quantity)]),
            sum([item_two.costs, (item_two.unit_value * item_two.quantity)]),
            sum([item_three.costs, (item_three.unit_value * item_three.quantity)])  # noqa
        ]) == payload.total_amount


class TestTradeNoteServiceDelete:

    @pytest.mark.asyncio
    @mock.patch.object(EventDoc, "delete_many")
    async def test_delete(self, delete_many, async_client):

        trade_note = await TradeNoteService().delete(
            "624b4f0e2b746ffa4848da79")

        assert trade_note is None

        delete_many.assert_awaited_once_with({
            '_id': {
                '$in': [
                    ObjectId('624b4f0e2b746ffa4848da77'),
                    ObjectId('624b4f0e2b746ffa4848da78')
                ]
            }
        })
