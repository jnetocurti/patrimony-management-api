from typing import List

from fastapi import (
    Depends,
    Response,
    APIRouter,
    HTTPException,
    BackgroundTasks
)

from app.core.business.assets.services import AssetService
from app.core.business.trade_notes.models import TradeNote, BaseTradeNote
from app.core.business.trade_notes.services import TradeNoteService

router = APIRouter(tags=["Trade Notes"], prefix="/trade_notes")


def assets_to_summarize(trade_note: TradeNote):
    return set([(i.asset_code, i.asset_type) for i in trade_note.note_items])


@router.get("/", response_model=List[TradeNote])
async def find_all(service: TradeNoteService = Depends()):

    return await service.find_all()


@router.get("/{id}", response_model=TradeNote)
async def get_by_id(id: str, service: TradeNoteService = Depends()):

    if subscription := await service.get(id):
        return subscription

    raise HTTPException(status_code=404)


@router.post("/", status_code=201, response_model=TradeNote)
async def create_a_trade_note(
    trade_note: BaseTradeNote,
    background_tasks: BackgroundTasks,
    service: TradeNoteService = Depends()
):
    trade_note = await service.create(trade_note)

    [background_tasks.add_task(AssetService.update_totals, i[0], i[1])
     for i in assets_to_summarize(trade_note)]

    return trade_note


@router.put("/{id}", response_model=TradeNote)
async def update_a_trade_note(
    id: str,
    trade_note: BaseTradeNote,
    background_tasks: BackgroundTasks,
    service: TradeNoteService = Depends()
):

    if old_trade_note := await service.get(id):

        old_assets = assets_to_summarize(old_trade_note)
        trade_note = await service.update(id, trade_note)

        [background_tasks.add_task(AssetService.update_totals, i[0], i[1])
         for i in (old_assets.union(assets_to_summarize(trade_note)))]

        return trade_note

    raise HTTPException(status_code=404)


@router.delete("/{id}", status_code=204)
async def delete_a_trade_note(
    id: str,
    background_tasks: BackgroundTasks,
    service: TradeNoteService = Depends()
):
    if trade_note := await service.get(id):

        await service.delete(id)
        [background_tasks.add_task(AssetService.update_totals, i[0], i[1])
         for i in (assets_to_summarize(trade_note))]

        return Response(status_code=204)

    raise HTTPException(status_code=404)
