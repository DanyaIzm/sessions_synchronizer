import datetime

from dto import UserSessionDTO
from models import UserSession


def map_user_sessions_to_dtos(
    user_sessions: list[UserSession], current_time: datetime.datetime
) -> list[UserSessionDTO]:
    return [
        UserSessionDTO(
            id=str(session.id),
            address=session.address,
            start_time=session.start_time,
            user_agent=session.user_agent,
            duration=current_time - session.start_time,
        )
        for session in user_sessions
    ]
