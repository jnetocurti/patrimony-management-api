from pytest_schema import exact_schema
from tests.api.schemas.commons import object_id_schema, asset_types_schema

asset_schema = exact_schema({
    "_id": object_id_schema,
    "quantity": 1,
    "asset_code": str,
    "asset_type": asset_types_schema,
    "total_acquisition_cost": float,
    "unit_acquisition_cost": float
})


assets_schema = exact_schema([asset_schema])
