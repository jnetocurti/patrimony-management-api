from app.core.utils.constants import EventType
from app.core.business.events.models import EventDoc


async def aggregate_to_assets(asset_code, asset_type):
    await EventDoc.collection.aggregate([
        {
            "$match": {
                "asset_code": asset_code,
                "asset_type": asset_type,
                "event_type": {
                    "$in": [EventType.SUBSCRIPTION.value]
                }
            }
        },
        {
            "$group": {
                "_id": ["$_id"],
                "asset_id": {"$first": "$asset_id"},
                "asset_code": {"$first": "$asset_code"},
                "asset_type": {"$first": "$asset_type"},
                "costs": {"$first": "$costs"},
                "quantity": {"$first": "$quantity"},
                "unit_value": {"$first": {
                    "$multiply": ["$unit_value", "$quantity"]}
                }
            }
        },
        {
            "$addFields": {
                "total_acquisition_cost": {"$add": ["$unit_value", "$costs"]}
            }
        },
        {
            "$group": {
                "_id": "$asset_id",
                "quantity": {"$sum": "$quantity"},
                "asset_code": {"$first": "$asset_code"},
                "asset_type": {"$first": "$asset_type"},
                "total_acquisition_cost": {"$sum": "$total_acquisition_cost"}
            }
        },
        {
            "$addFields": {
                "unit_acquisition_cost": {
                    "$divide": ["$total_acquisition_cost", "$quantity"]
                }
            }
        },
        {
            "$unset": ["unit_value", "costs"]
        },
        {
            "$merge": {"into": "assets", "on": "_id", "whenMatched": "replace"}
        }
    ]).to_list(None)
