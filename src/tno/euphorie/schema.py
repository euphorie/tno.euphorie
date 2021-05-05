from zope.interface import implementer
from zope.schema._bootstrapinterfaces import ValidationError
from zope.schema._field import NativeStringLine
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import INativeStringLine

import uuid


class InvalidUUID(ValidationError):
    __doc__ = "Dit is geen valide UUID."


class IUUID(INativeStringLine):
    """A field containing an UUID"""


@implementer(IUUID, IFromUnicode)
class UUID(NativeStringLine):
    """UUID schema field"""

    def _validate(self, value):
        super(UUID, self)._validate(value)
        try:
            uuid.UUID(value)
        except ValueError:
            raise InvalidUUID(value)

    def fromUnicode(self, value):
        v = str(value.strip())
        self.validate(v)
        return v
