from typing import List

from app.core.utils.constants import EventType
from app.core.utils.decorators import transactional
from app.core.business.assets.models import AssetDoc
from app.core.business.events.models import EventDoc
from app.core.business.subscriptions.models import (
    Subscription,
    PatchSubscription,
    CreateSubscription
)


class SubscriptionService:

    async def find_all(self) -> List[Subscription]:
        documents = EventDoc.find(event_type=EventType.SUBSCRIPTION)
        return [Subscription(**document.dump()) async for document in documents]  # noqa

    async def get(self, id: str) -> Subscription:
        document = await EventDoc.get(id)
        return Subscription(**document.dump()) if document else None

    @transactional
    async def create(self, subscription: CreateSubscription) -> Subscription:

        asset = await AssetDoc.get_or_create(
            subscription.asset_code, subscription.asset_type
        )
        event = EventDoc(
            asset_id=asset.pk,
            event_type=EventType.SUBSCRIPTION,
            **subscription.dict()
        )
        await event.save()

        return Subscription(**event.dump())

    async def update(
        self, id: str, subscription: PatchSubscription
    ) -> Subscription:

        if event := await EventDoc.get(id):
            await event.update(subscription.dict())
            return Subscription(**event.dump())

    # TODO corrigir problema agregação de totais na coleção asset
    # quando exclusão do último evento associado ao ativo
    async def delete(self, id: str) -> None:

        if event := await EventDoc.get(id):
            await event.delete()
