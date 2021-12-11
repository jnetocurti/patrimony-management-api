from typing import List

from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException

from app.core.business.assets.models import Asset
from app.core.business.assets.services import AssetService

router = APIRouter(tags=["Assets"], prefix="/assets")


@router.get("/", response_model=List[Asset])
async def find_all(service: AssetService = Depends()):

    return await service.find_all()


@router.get("/{id}", response_model=Asset)
async def get_by_id(id: str, service: AssetService = Depends()):

    if asset := await service.get(id):
        return asset

    raise HTTPException(status_code=404)
