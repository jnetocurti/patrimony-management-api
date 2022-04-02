import pytest
from mock import patch
from httpx import AsyncClient
from tests import ensure_builders
from fastapi import BackgroundTasks
from umongo.frameworks import MotorAsyncIOInstance

from app.main import app
from app.core.database import connection
from app.core.business.trade_notes.services import TradeNoteService
from app.core.business.subscriptions.services import SubscriptionService


@pytest.fixture(autouse=True)
def umongo_mock():
    with patch.object(
        MotorAsyncIOInstance, "is_compatible_with", return_value=True
    ) as mock:
        yield mock


@pytest.fixture()
def add_background_tasks_mock():
    with patch.object(BackgroundTasks, "add_task") as mock:
        yield mock


@pytest.fixture
async def async_client(async_mongodb):
    # set with mock mongodb
    connection.instance.set_db(async_mongodb)

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client

# Add dynamically builders to models
ensure_builders()

# workaround - limitation with transactional decorator mock... thanks python
TradeNoteService.create = TradeNoteService.create.__wrapped__
TradeNoteService.update = TradeNoteService.update.__wrapped__
TradeNoteService.delete = TradeNoteService.delete.__wrapped__
SubscriptionService.create = SubscriptionService.create.__wrapped__
