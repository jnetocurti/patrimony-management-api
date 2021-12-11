from app.core.business.assets.models import AssetDoc
from app.core.business.events.models import EventDoc


async def ensure_indexes():
    await AssetDoc.ensure_indexes()
    await EventDoc.ensure_indexes()
