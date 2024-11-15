import datetime
from typing import Protocol
from uuid import uuid4

from models import UserSession


class UserSessionsRepository(Protocol):
    def get_all_sessions(self) -> list[UserSession]: ...

    def add_session(self, session: UserSession) -> None: ...

    def remove_session(self, session: UserSession) -> None: ...


class UserSessionsService:
    def __init__(self, repository: UserSessionsRepository) -> None:
        self._repository = repository

    def get_sessions(self) -> list[UserSession]:
        return self._repository.get_all_sessions()

    def create_new_session(self, address: str, user_agent: str) -> UserSession:
        session_id = uuid4()
        start_time = datetime.datetime.now()

        user_session = UserSession(
            id=session_id,
            start_time=start_time,
            address=address,
            user_agent=user_agent,
        )

        self._repository.add_session(user_session)

        return user_session

    def destroy_session(self, session: UserSession) -> None:
        self._repository.remove_session(session)
