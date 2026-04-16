import enum

from pydantic import BaseModel

ID = int


class IDModel(BaseModel):
    id: ID

class SortDirections(enum.Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
