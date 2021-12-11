import pytest
from tests.api.schemas.commons import currency_types_schema


class TestCurrencyTypesFindAll:

    @pytest.mark.asyncio
    async def test_find_all(self, async_client):

        response = await async_client.get("/currency-types/")

        assert response.status_code == 200
        assert all([i == currency_types_schema.validate(i)
                   for i in response.json()])
