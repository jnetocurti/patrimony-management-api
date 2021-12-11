import pytest
from tests.api.schemas.commons import event_types_schema


class TestEventTypesFindAll:

    @pytest.mark.asyncio
    async def test_find_all(self, async_client):

        response = await async_client.get("/event-types/")

        assert response.status_code == 200
        assert all([i == event_types_schema.validate(i)
                   for i in response.json()])
