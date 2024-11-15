import datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserSession:
    id: UUID
    address: str
    start_time: datetime.datetime
    user_agent: str
