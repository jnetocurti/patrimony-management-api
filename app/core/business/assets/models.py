from typing import Type

from pydantic import Field

from app.core import connection
from app.core.utils import fields
from app.core.utils.fields import validate
from app.core.utils.constants import AssetType
from app.core.business.base_models import Document, DocumentIdMixin


class Asset(DocumentIdMixin):
    """
    Represents an asset saved in the database
    """
    asset_code: str = Field()
    asset_type: AssetType = Field()
    quantity: float = Field()
    total_acquisition_cost: float = Field()
    unit_acquisition_cost: float = Field()


@connection.instance.register
class AssetDoc(Document):
    """
    Persistent entity representing an asset
    """
    asset_code = fields.StringField(
        required=True, validate=validate.Length(min=1))
    asset_type = fields.EnumField(AssetType, required=True)
    quantity = fields.FloatField(default=0)
    total_acquisition_cost = fields.FloatField(default=0)
    unit_acquisition_cost = fields.FloatField(default=0)

    @classmethod
    def get_by_code_and_type(
        cls, asset_code: str, asset_type: AssetType
    ) -> Type["AssetDoc"]:

        return cls.find_one({
            "asset_type": asset_type, "asset_code": asset_code
        })

    @classmethod
    async def get_or_create(
        cls, asset_code: str, asset_type: AssetType
    ) -> Type["AssetDoc"]:

        if asset := await cls.get_by_code_and_type(asset_code, asset_type):
            return asset

        asset = cls(asset_code=asset_code, asset_type=asset_type)
        await asset.save()

        return asset

    class Meta:
        collection_name = "assets"
        indexes = ({'key': ['asset_type', 'asset_code'], 'unique': True},)
