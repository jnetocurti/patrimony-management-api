import functools
from typing import List
from datetime import date

from pydantic import Field, BaseModel

from app.core import connection
from app.core.utils import fields
from app.core.utils.fields import validate
from app.core.utils.constants import AssetType, EventType, CurrencyType
from app.core.business.base_models import (
    Document,
    DocumentIdMixin,
    EmbeddedDocument
)


class BaseTradeNoteItem(BaseModel):
    """
    Represents a trade note item for creation and update
    """
    asset_code: str = Field(min_length=1)
    asset_type: AssetType = Field()
    event_type: EventType = Field()
    quantity: float = Field(gt=0.00001)
    unit_value: float = Field(gt=0.01)

    @property
    def total_amount(self):
        return self.quantity * self.unit_value


class BaseTradeNote(BaseModel):
    """
    Represents a trade note for creation and update
    """
    note_id: str = Field(min_length=1)
    broker: str = Field(min_length=1)
    trade_date: date = Field()
    liquidate_date: date = Field()
    total_amount: float = Field(gt=0.01)
    currency: CurrencyType = Field()
    note_items: List[BaseTradeNoteItem] = Field(min_items=1)

    @property
    def liquid_total_amount(self):
        return functools.reduce(
            lambda ac, i: ac + i.total_amount, self.note_items, 0
        )

    @property
    def costs(self):
        return round((self.total_amount - self.liquid_total_amount), 6)

    @property
    def unit_cost_multiplier(self):
        return self.costs / self.liquid_total_amount


class TradeNoteItem(BaseTradeNoteItem):
    """
    Represents a trade note item saved in the database
    """
    costs: float = Field()


class TradeNote(BaseTradeNote, DocumentIdMixin):
    """
    Represents a trade note saved in the database
    """
    note_items: List[TradeNoteItem] = Field(min_items=1)


@connection.instance.register
class NoteItemDoc(EmbeddedDocument):
    """
    Persistent entity representing a note item
    """
    asset_code = fields.StringField(
        required=True, validate=validate.Length(min=1))
    asset_type = fields.EnumField(AssetType, required=True)
    event_type = fields.EnumField(EventType, required=True)
    quantity = fields.FloatField(
        required=True, validate=validate.Range(min=0.00001))
    unit_value = fields.FloatField(
        required=True, validate=validate.Range(min=0.01))
    costs = fields.FloatField()

    event_id = fields.ReferenceField("EventDoc", required=True, unique=True)


@connection.instance.register
class TradeNoteDoc(Document):
    """
    Persistent entity representing a trade note
    """
    note_id = fields.StringField(
        required=True, validate=validate.Length(min=1))
    broker = fields.StringField(required=True, validate=validate.Length(min=1))
    trade_date = fields.DateField(required=True)
    liquidate_date = fields.DateField(required=True)
    total_amount = fields.FloatField(
        required=True, validate=validate.Range(min=0.01))
    currency = fields.EnumField(CurrencyType, required=True)

    note_items = fields.ListField(fields.EmbeddedField(
        NoteItemDoc), required=True, validate=validate.Length(min=1))

    class Meta:
        collection_name = "trade-notes"
        indexes = ('note_id', 'trade_date',
                   'liquidate_date', 'note_items.asset_code')
