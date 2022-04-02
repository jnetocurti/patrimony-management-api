from typing import List

from app.core.utils.decorators import transactional
from app.core.business.assets.models import AssetDoc
from app.core.business.events.models import EventDoc
from app.core.business.trade_notes.models import (
    TradeNote,
    NoteItemDoc,
    TradeNoteDoc,
    BaseTradeNote
)


class TradeNoteService:

    async def find_all(self) -> List[TradeNote]:
        documents = TradeNoteDoc.find()
        return [TradeNote(**document.dump()) async for document in documents]

    async def get(self, id: str) -> TradeNote:
        document = await TradeNoteDoc.get(id)
        return TradeNote(**document.dump()) if document else None

    @transactional
    async def create(self, trade_note: BaseTradeNote) -> TradeNote:

        document = TradeNoteDoc(**trade_note.dict())
        document.note_items = await self._create_items(trade_note)
        await document.save()

        return TradeNote(**document.dump())

    @transactional
    async def update(self, id: str, trade_note: BaseTradeNote) -> TradeNote:

        if document := await TradeNoteDoc.get(id):

            await self._update_items(document, trade_note)
            await document.update(trade_note.dict(exclude={"note_items"}))

            return TradeNote(**document.dump())

    @transactional
    async def delete(self, id: str) -> None:

        if document := await TradeNoteDoc.get(id):
            await self._delete_items_events(document)
            await document.delete()

    async def _create_items(self, trade_note: BaseTradeNote):

        items = []
        for item in trade_note.note_items:

            asset = await AssetDoc.get_or_create(
                item.asset_code, item.asset_type
            )
            costs = round(
                trade_note.unit_cost_multiplier * item.total_amount, 6
            )
            item_event = EventDoc(
                asset_id=asset.pk,
                broker=trade_note.broker,
                event_date=trade_note.trade_date,
                effective_event_date=trade_note.liquidate_date,
                currency=trade_note.currency,
                costs=costs,
                **item.dict()
            )
            await item_event.save()

            items.append(NoteItemDoc(
                event_id=item_event.pk, costs=costs, **item.dict()
            ))

        return items

    async def _update_items(self, document: TradeNoteDoc, model: BaseTradeNote):  # noqa

        await self._delete_items_events(document)
        document.note_items = await self._create_items(model)

    async def _delete_items_events(self, document: TradeNoteDoc):

        await EventDoc.delete_many({
            "_id": {
                "$in": [i.event_id.pk for i in document.note_items]
            }
        })
