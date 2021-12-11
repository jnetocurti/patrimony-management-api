import pytest
from tests.api.schemas.assets import asset_schema, assets_schema
from tests.api.schemas.commons import not_found_schema


class TestAssetsFindAll:

    @pytest.mark.asyncio
    async def test_find_all(self, async_client):

        response = await async_client.get("/assets/")

        assert response.status_code == 200
        assert response.json() == assets_schema


class TestAssetsGetById:

    @pytest.mark.asyncio
    async def test_get_by_id(self, async_client):

        response = await async_client.get("/assets/62476a58784e762f7310eaf1")

        assert response.status_code == 200
        assert response.json() == asset_schema

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, async_client):

        response = await async_client.get("/assets/1fae0137f267e48785a67426")

        assert response.status_code == 404
        assert response.json() == not_found_schema
