import datetime
from functools import cache
import logging
import sqlite3

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from pydantic_core import to_jsonable_python
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from mappers import map_user_sessions_to_dtos
from repositories import SQLiteRepository
from services import UserSessionsRepository, UserSessionsService

app = FastAPI()

logger = logging.getLogger("uvicorn.error")


@cache
def get_user_sessions_repository():
    sqlite_connection = sqlite3.connect("database.db", check_same_thread=False)
    repository = SQLiteRepository(connection=sqlite_connection)

    return repository


def get_user_sessions_service(
    repository: UserSessionsRepository = Depends(get_user_sessions_repository),
) -> UserSessionsService:
    return UserSessionsService(repository=repository)


app.mount("/static", StaticFiles(directory="static", html=True), name="site")


@app.get("/")
def index() -> FileResponse:
    return FileResponse("./templates/index.html")


@app.websocket("/ws")
async def websocket_handler(
    websocket: WebSocket,
    user_sessions_service: UserSessionsService = Depends(get_user_sessions_service),
) -> None:
    await websocket.accept()

    address = f"{websocket.client.host}:{websocket.client.port}"
    user_agent = websocket.headers.get("user-agent")

    user_session = user_sessions_service.create_new_session(address, user_agent)

    logger.info(f"New user session: {user_session}")

    try:
        while True:
            message = await websocket.receive_text()

            match message:
                case "get_all_sessions":
                    await websocket.send_json(
                        to_jsonable_python(
                            map_user_sessions_to_dtos(
                                user_sessions_service.get_sessions(),
                                datetime.datetime.now(),
                            )
                        )
                    )
                case _:
                    await websocket.send_json({"error": "unknown command"})

    except WebSocketDisconnect:
        user_sessions_service.destroy_session(user_session)
        logger.info(f"User disconnected: {user_session}")
