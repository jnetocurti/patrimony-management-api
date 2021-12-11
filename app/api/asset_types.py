from typing import List

from fastapi import APIRouter

from app.core.utils.constants import AssetType

router = APIRouter(tags=["Asset Types"], prefix="/asset-types")


@router.get("/", response_model=List[AssetType])
def find_all():
    return [i.value for i in AssetType]
