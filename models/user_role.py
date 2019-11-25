from enum import (
    Enum,
    auto,
)

from utils import log


class UserRole(Enum):
    guest = auto()
    normal = auto()

    def translate(self, _escape_table):
        log('UserRole translate <{}> <{}>'.format(_escape_table, type(_escape_table)))
        return self.name

# enum UserRole:
#     guest
#     normal
