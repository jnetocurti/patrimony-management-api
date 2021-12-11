from umongo import Document as UmongoDocument
from umongo import EmbeddedDocument  # noqa
from pydantic import Field, BaseModel
from bson.objectid import ObjectId

from app.core import connection


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise TypeError("invalid ObjectId")
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DocumentIdMixin(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


@connection.instance.register
class Document(UmongoDocument):

    def save(cls):
        return cls.commit()

    def update(cls, data):
        cls._data.update(data)
        return cls.save()

    @classmethod
    def get(cls, id):
        return cls.find_one(cls._get_id_query(id))

    @classmethod
    def find(cls, **filter):
        return super(Document, cls).find(filter)

    @classmethod
    def _get_id_query(cls, id):
        return ObjectId(id) if cls._is_valid_objectid(id) else id

    @classmethod
    def _is_valid_objectid(cls, id):
        return isinstance(id, str) and ObjectId.is_valid(id)

    class Meta:
        abstract = True
