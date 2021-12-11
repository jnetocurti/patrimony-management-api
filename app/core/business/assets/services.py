from typing import List

from app.core.business.assets.models import Asset, AssetDoc


class AssetService:

    async def find_all(self) -> List[Asset]:
        return [Asset(**document.dump()) async for document in AssetDoc.find()]

    async def get(self, id: str) -> Asset:
        document = await AssetDoc.get(id)
        return Asset(**document.dump()) if document else None
