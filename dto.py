import datetime

from pydantic import BaseModel

from helpers import format_timedelta_to_short_string


class UserSessionDTO(BaseModel):
    id: str
    address: str
    start_time: datetime.datetime
    user_agent: str
    duration: datetime.timedelta

    class Config:
        json_encoders = {
            datetime.datetime: lambda x: x.strftime("%H:%M:%S"),
            datetime.timedelta: format_timedelta_to_short_string,
        }
