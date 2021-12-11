from typing import List

from fastapi import (
    Depends,
    Response,
    APIRouter,
    HTTPException,
    BackgroundTasks
)

from app.core.business.events.aggregations import aggregate_to_assets
from app.core.business.subscriptions.models import (
    Subscription,
    PatchSubscription,
    CreateSubscription
)
from app.core.business.subscriptions.services import SubscriptionService

router = APIRouter(tags=["Subscriptions"], prefix="/assets/subscriptions")


@router.get("/", response_model=List[Subscription])
async def find_all(service: SubscriptionService = Depends()):

    return await service.find_all()


@router.get("/{id}", response_model=Subscription)
async def get_by_id(id: str, service: SubscriptionService = Depends()):

    if subscription := await service.get(id):
        return subscription

    raise HTTPException(status_code=404)


@router.post("/", status_code=201, response_model=Subscription)
async def create_a_subscription(
    subscription: CreateSubscription,
    background_tasks: BackgroundTasks,
    service: SubscriptionService = Depends()
):
    subscription = await service.create(subscription)

    background_tasks.add_task(
        aggregate_to_assets,
        subscription.asset_code,
        subscription.asset_type.value
    )

    return subscription


@router.patch("/{id}", response_model=Subscription)
async def partially_update_a_subscription(
    id: str,
    subscription: PatchSubscription,
    background_tasks: BackgroundTasks,
    service: SubscriptionService = Depends()
):
    if subscription := await service.update(id, subscription):
        background_tasks.add_task(
            aggregate_to_assets,
            subscription.asset_code,
            subscription.asset_type.value
        )
        return subscription

    raise HTTPException(status_code=404)


@router.delete("/{id}", status_code=204)
async def delete_a_subscription(
    id: str,
    background_tasks: BackgroundTasks,
    service: SubscriptionService = Depends()
):
    if subscription := await service.get(id):
        asset_code, asset_type = (
            subscription.asset_code, subscription.asset_type.value)
        await service.delete(id)

        background_tasks.add_task(aggregate_to_assets, asset_code, asset_type)
        return Response(status_code=204)

    raise HTTPException(status_code=404)
