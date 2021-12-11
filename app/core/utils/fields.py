from umongo import validate  # noqa F401
from marshmallow import ValidationError
from umongo.fields import (  # noqa F401
    BaseField,
    DateField,
    ListField,
    FloatField,
    StringField,
    IntegerField,
    EmbeddedField,
    ObjectIdField,
    ReferenceField
)


class EnumField(BaseField):

    def __init__(self, enum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum = enum

    def _deserialize(self, obj, attr, data, **kwargs):

        if isinstance(obj, self.enum):
            return obj.value

        try:
            return self.enum(obj).value
        except:  # noqa E722
            raise ValidationError(f"Invalid value '{obj}' for {self.enum}")
