import logging 

logger = logging.getLogger(__name__)


from pydantic import BaseModel


class Player(BaseModel):
    name: str
    age: int
    nationality: str
    club: str
    matches: int
    goals: int
    trophys: list[str]
    