from typing import Optional
from datetime import date

from pydantic import Field, BaseModel

from app.core import connection
from app.core.utils import fields
from app.core.utils.fields import validate
from app.core.utils.constants import AssetType, EventType, CurrencyType
from app.core.business.base_models import Document, DocumentIdMixin


class BaseCreateEvent(BaseModel):
    """
    Represents a portfolio event with common fields for creation
    """
    broker: str = Field(min_length=1)
    event_date: date = Field()
    asset_type: AssetType = Field()
    asset_code: str = Field(min_length=1)
    quantity: float = Field(gt=0.00001)
    unit_value: float = Field(gt=0.01)
    costs: Optional[float] = Field()
    currency: CurrencyType = Field()
    note: Optional[str] = Field()

    class Config:
        allow_population_by_field_name = True


class BaseCreateEventExtras(BaseCreateEvent):
    """
    Represents a portfolio event with all fields for creation
    """
    event_type: EventType = Field()
    asset_derived_code: Optional[str] = Field(min_length=1)
    effective_event_date: Optional[date] = Field()


class BasePatchEvent(BaseCreateEvent):
    """
    Represents a portfolio event with common fields to update
    """
    broker: Optional[str] = Field(min_length=1)
    event_date: Optional[date] = Field()
    asset_type: Optional[AssetType] = Field()
    asset_code: Optional[str] = Field(min_length=1)
    quantity: Optional[float] = Field(gt=0.00001)
    unit_value: Optional[float] = Field(gt=0.01)
    currency: Optional[CurrencyType] = Field()

    def dict(self, *args, **kwargs):
        return super().dict(*args, exclude_unset=True, **kwargs)


class BasePatchEventExtras(BasePatchEvent):
    """
    Represents a portfolio event with all fields to update
    """
    event_type: Optional[EventType] = Field()
    asset_derived_code: Optional[str] = Field(min_length=1)
    effective_event_date: Optional[date] = Field()


class Event(BaseCreateEventExtras, DocumentIdMixin):
    """
    Represents a portfolio event saved in the database
    """


@connection.instance.register
class EventDoc(Document):
    """
    Persistent entity representing a portfolio event
    """
    broker = fields.StringField(required=True, validate=validate.Length(min=1))
    event_type = fields.EnumField(EventType, required=True)
    event_date = fields.DateField(required=True)
    effective_event_date = fields.DateField()
    asset_code = fields.StringField(
        required=True, validate=validate.Length(min=1))
    asset_derived_code = fields.StringField(validate=validate.Length(min=1))
    asset_type = fields.EnumField(AssetType, required=True)
    quantity = fields.FloatField(
        required=True, validate=validate.Range(min=0.00001))
    unit_value = fields.FloatField(
        required=True, validate=validate.Range(min=0.01))
    costs = fields.FloatField()
    currency = fields.EnumField(CurrencyType, required=True)
    note = fields.StringField()

    asset_id = fields.ReferenceField("AssetDoc", required=True)

    class Meta:
        collection_name = "events"
        indexes = ('asset_type', 'asset_code', 'event_date')
