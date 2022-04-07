import pytest
from fastapi.encoders import jsonable_encoder
from tests.api.schemas.commons import not_found_schema
from tests.api.schemas.subscriptions import (
    subscription_schema,
    subscriptions_schema
)

from app.core.business.assets.services import AssetService
from app.core.business.subscriptions.models import BaseSubscription


class TestSubscriptionsFindAll:

    @pytest.mark.asyncio
    async def test_find_all(self, async_client):

        response = await async_client.get("/assets/subscriptions/")

        assert response.status_code == 200
        assert response.json() == subscriptions_schema


class TestSubscriptionsGetById:

    @pytest.mark.asyncio
    async def test_get_by_id(self, async_client):

        response = await async_client.get(
            "/assets/subscriptions/62476a58784e762f7310eaf2")

        assert response.status_code == 200
        assert response.json() == subscription_schema

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, async_client):

        response = await async_client.get(
            "/assets/subscriptions/2fae0137f267e48785a67426")

        assert response.status_code == 404
        assert response.json() == not_found_schema


class TestSubscriptionsCreateASubscription:

    @pytest.mark.asyncio
    async def test_create_a_subscription(
        self, async_client, add_background_tasks_mock
    ):

        payload = jsonable_encoder(
            BaseSubscription.builder().build()
        )

        response = await async_client.post(
            "/assets/subscriptions/", json=payload)

        add_background_tasks_mock.assert_called_once_with(
            AssetService.update_totals, "xpto11", "BRL_STOCKS")

        assert response.status_code == 201
        assert response.json() == subscription_schema


class TestSubscriptionsPartiallyUpdateASubscription:

    @pytest.mark.asyncio
    async def test_partially_update_a_subscription(
        self, async_client, add_background_tasks_mock
    ):

        payload = jsonable_encoder(
            BaseSubscription.builder().with_asset_code("XPTO3").build()
        )

        response = await async_client.patch(
            "/assets/subscriptions/62476a58784e762f7310eaf2", json=payload)

        add_background_tasks_mock.assert_called_once_with(
            AssetService.update_totals, 'XPTO3', 'BRL_STOCKS')

        assert response.status_code == 200
        assert response.json() == subscription_schema

    @pytest.mark.asyncio
    async def test_partially_update_a_subscription_not_found(
        self, async_client, add_background_tasks_mock
    ):

        payload = jsonable_encoder(
            BaseSubscription.builder().build()
        )

        response = await async_client.patch(
            "/assets/subscriptions/2fae0137f267e48785a67426", json=payload)

        add_background_tasks_mock.assert_not_called()

        assert response.status_code == 404
        assert response.json() == not_found_schema


class TestSubscriptionsDeleteASubscription:

    @pytest.mark.asyncio
    async def test_delete_a_subscription(
        self, async_client, add_background_tasks_mock
    ):

        response = await async_client.delete(
            "/assets/subscriptions/62476a58784e762f7310eaf2")

        add_background_tasks_mock.assert_called_once_with(
            AssetService.update_totals, 'XPTO3', 'BRL_STOCKS')

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_a_subscription_not_found(
        self, async_client, add_background_tasks_mock
    ):

        response = await async_client.delete(
            "/assets/subscriptions/2fae0137f267e48785a67426")

        add_background_tasks_mock.assert_not_called()

        assert response.status_code == 404
        assert response.json() == not_found_schema
