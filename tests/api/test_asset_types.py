import pytest
from tests.api.schemas.commons import asset_types_schema


class TestAssetTypesFindAll:

    @pytest.mark.asyncio
    async def test_find_all(self, async_client):

        response = await async_client.get("/asset-types/")

        assert response.status_code == 200
        assert all([i == asset_types_schema.validate(i)
                   for i in response.json()])
