from pytest_schema import exact_schema
from tests.api.schemas.commons import (
    date_schema,
    object_id_schema,
    asset_types_schema,
    event_types_schema,
    currency_types_schema
)

trade_note_schema = exact_schema({
    "_id": object_id_schema,
    "note_id": str,
    "broker": str,
    "trade_date": date_schema,
    "liquidate_date": date_schema,
    "total_amount": float,
    "currency": currency_types_schema,
    "note_items": [
        {
            "asset_code": str,
            "asset_type": asset_types_schema,
            "event_type": event_types_schema,
            "quantity": float,
            "unit_value": float,
            "costs": float
        }
    ]
})

trade_notes_schema = exact_schema([trade_note_schema])
