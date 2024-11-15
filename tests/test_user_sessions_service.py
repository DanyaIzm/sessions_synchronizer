from services import UserSessionsService
from repositories import MemoryUserSessionsRepository
import unittest


class TestUserSessionsService(unittest.TestCase):
    def test_create_sessions(self):
        repo = MemoryUserSessionsRepository()
        service = UserSessionsService(repo)

        session1 = service.create_new_session(address="123", user_agent="safari?")
        session2 = service.create_new_session(address="456", user_agent="chromium")

        sessions = service.get_sessions()

        self.assertEqual(len(sessions), 2)

        self.assertEqual(sessions[0].address, "123")
        self.assertEqual(sessions[0].user_agent, "safari?")

        self.assertEqual(sessions[1].address, "456")
        self.assertEqual(sessions[1].user_agent, "chromium")

        self.assertIn(session1, sessions)
        self.assertIn(session2, sessions)

    def test_destroy_sessions(self):
        repo = MemoryUserSessionsRepository()
        service = UserSessionsService(repo)

        session1 = service.create_new_session(address="123", user_agent="safari?")
        session2 = service.create_new_session(address="456", user_agent="chromium")

        sessions = service.get_sessions()

        service.destroy_session(session1)

        self.assertEqual(len(sessions), 1)

        self.assertEqual(sessions[0].address, "456")
        self.assertEqual(sessions[0].user_agent, "chromium")

        self.assertNotIn(session1, sessions)
        self.assertIn(session2, sessions)
