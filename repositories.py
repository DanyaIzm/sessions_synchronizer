import datetime
from sqlite3 import Connection
from uuid import UUID

from models import UserSession


class SQLiteRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection
        self._create_table()
        self._clear_table()

    def get_all_sessions(self) -> list[UserSession]:
        cursor = self._connection.execute(
            "SELECT * FROM UserSession ORDER BY start_time ASC"
        )
        res = [
            UserSession(
                id=UUID(row[0]),
                address=row[1],
                start_time=datetime.datetime.fromisoformat(row[2]),
                user_agent=row[3],
            )
            for row in cursor.fetchall()
        ]
        return res

    def add_session(self, session: UserSession) -> None:
        self._connection.execute(
            "INSERT INTO UserSession VALUES(?, ?, ?, ?)",
            (
                str(session.id),
                session.address,
                session.start_time,
                session.user_agent,
            ),
        )
        self._connection.commit()

    def remove_session(self, session: UserSession) -> None:
        self._connection.execute(
            "DELETE FROM UserSession WHERE id=?", (str(session.id),)
        )
        self._connection.commit()

    def _create_table(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS UserSession (
            id TEXT PRIMARY KEY,
            address TEXT NOT NULL,
            start_time TEXT NOT NULL,
            user_agent TEXT NOT NULL 
            );
            """
        )
        self._connection.commit()

    def _clear_table(self) -> None:
        self._connection.execute("DELETE FROM UserSession")
        self._connection.commit()


class MemoryUserSessionsRepository:
    def __init__(self) -> None:
        self._sessions: list[UserSession] = []

    def get_all_sessions(self) -> list[UserSession]:
        return self._sessions

    def add_session(self, session: UserSession) -> None:
        self._sessions.append(session)
        self._sort_sessions()

    def remove_session(self, session: UserSession) -> None:
        self._sessions.remove(session)
        self._sort_sessions()

    def _sort_sessions(self) -> None:
        self._sessions.sort(key=lambda s: s.start_time)
