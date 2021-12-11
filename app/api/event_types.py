from typing import List

from fastapi import APIRouter

from app.core.utils.constants import EventType

router = APIRouter(tags=["Event Types"], prefix="/event-types")


@router.get("/", response_model=List[EventType])
def find_all():
    return [i.value for i in EventType]
