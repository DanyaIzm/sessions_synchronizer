from main import app, get_user_sessions_repository
from fastapi.testclient import TestClient
import unittest

from repositories import MemoryUserSessionsRepository


class TestWebsocket(unittest.TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_user_sessions_repository] = (
            lambda: MemoryUserSessionsRepository()
        )

    def test_unknown_command(self):
        client = TestClient(app)

        with client.websocket_connect("/ws") as websocket:
            websocket.send_text("Unknown command?")

            response = websocket.receive_json()

            self.assertEqual(response, {"error": "unknown command"})

    def test_main_functionality(self):
        client = TestClient(app)

        with client.websocket_connect("/ws") as websocket:
            websocket.send_text("get_all_sessions")

            response = websocket.receive_json()

            self.assertEqual(len(response), 1)
            self.assertEqual(response[0]["address"], "testclient:50000")
