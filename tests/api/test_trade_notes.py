import pytest
from fastapi.encoders import jsonable_encoder
from tests.api.schemas.commons import not_found_schema
from tests.api.schemas.trade_note_schema import (
    trade_note_schema,
    trade_notes_schema
)

from app.core.business.assets.services import AssetService
from app.core.business.trade_notes.models import (
    BaseTradeNote,
    BaseTradeNoteItem
)


class TestTradeNoteFindAll:

    @pytest.mark.asyncio
    async def test_find_all(self, async_client):

        response = await async_client.get("/trade_notes/")

        assert response.status_code == 200
        assert response.json() == trade_notes_schema


class TestTradeNoteGetById:

    @pytest.mark.asyncio
    async def test_get_by_id(self, async_client):

        response = await async_client.get(
            "/trade_notes/624b4f0e2b746ffa4848da79")

        assert response.status_code == 200
        assert response.json() == trade_note_schema

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, async_client):

        response = await async_client.get(
            "/trade_notes/97ad8484aff647b2e0f4b426")

        assert response.status_code == 404
        assert response.json() == not_found_schema


class TestTradeNoteServiceCreateATradeNote:

    @pytest.mark.asyncio
    async def test_create_a_trade_note(
        self, async_client, add_background_tasks_mock
    ):

        payload = jsonable_encoder(
            BaseTradeNote.builder().build().dict()
        )

        response = await async_client.post("/trade_notes/", json=payload)

        add_background_tasks_mock.assert_called_once_with(
            AssetService.update_totals, "xpto11", "BRL_STOCKS")

        assert response.status_code == 201
        assert response.json() == trade_note_schema


class TestTradeNoteServiceUpdateATradeNote:

    @pytest.mark.asyncio
    async def test_update_a_trade_note(
        self, async_client, add_background_tasks_mock
    ):

        payload = jsonable_encoder(
            BaseTradeNote.builder()
            .with_note_items([
                BaseTradeNoteItem.builder().with_asset_code("XPTO3").build()
            ]).build().dict()
        )

        response = await async_client.put(
            "/trade_notes/624b4f0e2b746ffa4848da79", json=payload
        )

        add_background_tasks_mock.assert_called_once_with(
            AssetService.update_totals, "XPTO3", "BRL_STOCKS")

        assert response.status_code == 200
        assert response.json() == trade_note_schema

    @pytest.mark.asyncio
    async def test_update_a_trade_note_not_found(
        self, async_client, add_background_tasks_mock
    ):

        payload = jsonable_encoder(
            BaseTradeNote.builder().build().dict()
        )

        response = await async_client.put(
            "/trade_notes/97ad8484aff647b2e0f4b426", json=payload
        )

        add_background_tasks_mock.assert_not_called()

        assert response.status_code == 404
        assert response.json() == not_found_schema


class TestTradeNoteServiceDeleteATradeNote:

    @pytest.mark.asyncio
    async def test_delete_a_trade_note(
        self, async_client, add_background_tasks_mock
    ):

        response = await async_client.delete(
            "/trade_notes/624b4f0e2b746ffa4848da79")

        add_background_tasks_mock.assert_called_once_with(
            AssetService.update_totals, "XPTO3", "BRL_STOCKS")

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_a_trade_note_not_found(
        self, async_client, add_background_tasks_mock
    ):

        response = await async_client.delete(
            "/trade_notes/97ad8484aff647b2e0f4b426")

        add_background_tasks_mock.assert_not_called()

        assert response.status_code == 404
        assert response.json() == not_found_schema
