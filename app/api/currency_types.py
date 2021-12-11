from typing import List

from fastapi import APIRouter

from app.core.utils.constants import CurrencyType

router = APIRouter(tags=["Currency Types"], prefix="/currency-types")


@router.get("/", response_model=List[CurrencyType])
def find_all():
    return [i.value for i in CurrencyType]
