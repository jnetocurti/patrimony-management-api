from app.core.business.assets.models import AssetDoc
from app.core.business.events.models import EventDoc
from app.core.business.trade_notes.models import TradeNoteDoc


async def ensure_indexes():
    await AssetDoc.ensure_indexes()
    await EventDoc.ensure_indexes()
    await TradeNoteDoc.ensure_indexes()
