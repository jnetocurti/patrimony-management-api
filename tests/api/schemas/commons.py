from datetime import date

from bson.objectid import ObjectId
from pytest_schema import Or

from app.core.utils.constants import AssetType, EventType, CurrencyType

date_schema = (lambda i: date)

optional_str_schema = Or(str, None)

object_id_schema = (lambda i: ObjectId)

asset_types_schema = Or(*[i.value for i in AssetType])

currency_types_schema = Or(*[i.value for i in CurrencyType])

event_types_schema = Or(*[i.value for i in EventType])

not_found_schema = {'detail': 'Not Found'}
