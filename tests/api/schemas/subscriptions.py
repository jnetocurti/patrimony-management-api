from pytest_schema import exact_schema
from tests.api.schemas.commons import (
    date_schema,
    object_id_schema,
    asset_types_schema,
    optional_str_schema,
    currency_types_schema
)

subscription_schema = exact_schema({
    '_id': object_id_schema,
    'broker': str,
    'subscription_date': date_schema,
    'asset_type': asset_types_schema,
    'asset_code': str,
    'quantity': float,
    'unit_value': float,
    'costs': float,
    'currency': currency_types_schema,
    'note': optional_str_schema,
    'receipt_conversion_date': date_schema,
    'subscription_code': str
})

subscriptions_schema = exact_schema([subscription_schema])
