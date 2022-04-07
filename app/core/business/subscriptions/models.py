from typing import Optional
from datetime import date

from pydantic import Field

from app.core.business.base_models import DocumentIdMixin
from app.core.business.events.models import BasePatchEvent, BaseCreateEvent


class BaseSubscription(BaseCreateEvent):
    """
    Represents a subscription event
    """
    event_date: date = Field(alias="subscription_date")
    effective_event_date: date = Field(alias="receipt_conversion_date")
    asset_derived_code: str = Field(min_length=1, alias="subscription_code")


class CreateSubscription(BaseSubscription):
    """
    Represents a subscription event to be create
    """


class PatchSubscription(BasePatchEvent):
    """
    Represents a subscription event
    """
    event_date: Optional[date] = Field(alias="subscription_date")
    effective_event_date: Optional[date] = Field(
        alias="receipt_conversion_date")
    asset_derived_code: Optional[str] = Field(
        min_length=1, alias="subscription_code")


class Subscription(CreateSubscription, DocumentIdMixin):
    """
    Represents a subscription event saved in the database
    """
