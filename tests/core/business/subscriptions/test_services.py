from datetime import date

import pytest

from app.core.utils.constants import AssetType, CurrencyType
from app.core.business.subscriptions.models import BaseSubscription
from app.core.business.subscriptions.services import SubscriptionService


class TestSubscriptionServiceCreate:

    @pytest.mark.asyncio
    async def test_create(self, async_client):

        payload = BaseSubscription.builder()\
            .with_broker("Avenue")\
            .with_event_date(date(2022, 4, 8))\
            .with_effective_event_date(date(2022, 4, 8))\
            .with_asset_code("SDIV")\
            .with_asset_type(AssetType.USA_ETF)\
            .with_asset_derived_code("SDIV2")\
            .with_quantity(7)\
            .with_unit_value(146)\
            .with_costs(0.4)\
            .with_currency(CurrencyType.USD)\
            .with_note("2 SDIV ETF").build()

        subscription = await SubscriptionService().create(payload)

        assert subscription.id is not None
        assert subscription.broker == payload.broker
        assert subscription.event_date == payload.event_date
        assert subscription.effective_event_date == payload.effective_event_date  # noqa
        assert subscription.asset_code == payload.asset_code
        assert subscription.asset_type == payload.asset_type
        assert subscription.asset_derived_code == payload.asset_derived_code
        assert subscription.quantity == payload.quantity
        assert subscription.unit_value == payload.unit_value
        assert subscription.costs == payload.costs
        assert subscription.currency == payload.currency
        assert subscription.note == payload.note


class TestSubscriptionServiceUpdate:

    @pytest.mark.asyncio
    async def test_update(self, async_client):

        payload = BaseSubscription.builder()\
            .with_broker("Avenue")\
            .with_event_date(date(2022, 4, 8))\
            .with_effective_event_date(date(2022, 4, 8))\
            .with_asset_code("SDIV")\
            .with_asset_type(AssetType.USA_ETF)\
            .with_asset_derived_code("SDIV2")\
            .with_quantity(7)\
            .with_unit_value(146)\
            .with_costs(0.4)\
            .with_currency(CurrencyType.USD)\
            .with_note("2 SDIV ETF").build()

        subscription = await SubscriptionService().update(
            "62476a58784e762f7310eaf2", payload
        )

        assert subscription.id == "62476a58784e762f7310eaf2"
        assert subscription.broker == payload.broker
        assert subscription.event_date == payload.event_date
        assert subscription.effective_event_date == payload.effective_event_date  # noqa
        assert subscription.asset_code == payload.asset_code
        assert subscription.asset_type == payload.asset_type
        assert subscription.asset_derived_code == payload.asset_derived_code
        assert subscription.quantity == payload.quantity
        assert subscription.unit_value == payload.unit_value
        assert subscription.costs == payload.costs
        assert subscription.currency == payload.currency
        assert subscription.note == payload.note


class TestSubscriptionServiceDelete:

    @pytest.mark.asyncio
    async def test_delete(self, async_client):

        subscription = await SubscriptionService().delete(
            "62476a58784e762f7310eaf2")

        assert subscription is None
