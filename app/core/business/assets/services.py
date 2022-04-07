from typing import List

from app.core.utils.constants import AssetType, EventType
from app.core.business.assets.models import Asset, AssetDoc
from app.core.business.events.models import EventDoc


class AssetService:

    async def find_all(self) -> List[Asset]:
        return [Asset(**document.dump()) async for document in AssetDoc.find()]

    async def get(self, id: str) -> Asset:
        document = await AssetDoc.get(id)
        return Asset(**document.dump()) if document else None

    @classmethod
    async def update_totals(cls, asset_code: str, asset_type: AssetType):
        """
        Update quantity, unit acquisition cost and total acquisition cost
        """

        # Ensure aggregation or reset of totals
        if not await cls._check_update_totals(asset_code, asset_type):
            return

        aggregation = EventDoc.collection.aggregate([

            # Filter by asset_code, asset_type and elements that change totals
            {'$match': {
                'asset_code': asset_code,
                'asset_type': asset_type,
                '$or': [
                    {'event_type': {
                        '$in': [EventType.BUY, EventType.SALE]
                    }},
                    {'$and': [
                        {'event_type': {'$eq': EventType.SUBSCRIPTION}},
                        {'effective_event_date': {'$exists': True, '$ne': None}}  # noqa
                    ]}
                ]
            }},

            # Map/Add the required fields
            {'$project': {
                '_id': 1,
                'asset_id': 1,
                'costs': 1,
                'quantity': 1,
                'unit_value': 1,
                'event_type': 1,
                'total_value': {'$add': [
                    '$costs', {'$multiply': ['$quantity', '$unit_value']}
                ]}
            }},

            # Calculate totals by event types
            {"$group": {
                "_id": "$event_type",
                "asset_id": {"$first": "$asset_id"},
                "quantity": {"$sum": "$quantity"},
                "total_value": {"$sum": "$total_value"}
            }},

            # Calculate totals (sales, acquisition)
            {"$group": {
                "_id": "$asset_id",

                "total_sale_quantity": {"$sum": {
                    "$cond": [{"$in": [
                        "$_id", [EventType.SALE]
                    ]}, "$quantity", 0]
                }},

                "total_acquisition_quantity": {"$sum": {
                    "$cond": [{"$in": [
                        "$_id", [EventType.BUY, EventType.SUBSCRIPTION]
                    ]}, "$quantity", 0]
                }},

                "total_acquisition_value": {"$sum": {
                    "$cond": [{"$in": [
                        "$_id", [EventType.BUY, EventType.SUBSCRIPTION]
                    ]}, "$total_value", 0]
                }}
            }},

            # Calculate current quantity and unit acquisition cost
            {"$project": {
                "quantity": {"$subtract": [
                    "$total_acquisition_quantity", "$total_sale_quantity"
                ]},
                "unit_acquisition_cost": {"$divide": [
                    "$total_acquisition_value", "$total_acquisition_quantity"
                ]}
            }},

            # Calculate current total acquisition cost
            {"$set": {
                "total_acquisition_cost": {
                    "$multiply": ["$quantity", "$unit_acquisition_cost"]
                }
            }},

            # Merge into assets
            {"$merge": {
                "into": "assets",
                "on": "_id",
                "whenMatched": "merge",
                "whenNotMatched": "discard"
            }}
        ])

        await aggregation.to_list(None)

    @classmethod
    async def _check_update_totals(cls, asset_code: str, asset_type: AssetType) -> bool:  # noqa

        events_to_calculate = [
            EventType.BUY, EventType.SALE, EventType.SUBSCRIPTION
        ]

        has_events_to_calculate = await EventDoc.find(
            asset_code=asset_code,
            asset_type=asset_type,
            event_type={"$in": events_to_calculate}
        ).limit(1).to_list(None)

        if has_events_to_calculate:
            return True

        if asset := await AssetDoc.get_by_code_and_type(
                asset_code, asset_type):

            await asset.update(
                quantity=0, unit_acquisition_cost=0, total_acquisition_cost=0
            )
