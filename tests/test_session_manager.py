import unittest
import time
from datetime import datetime
from unittest.mock import patch


class TestSessionManager(unittest.TestCase):
    def test_session_manager_creation(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        self.assertEqual(len(manager.sessions), 0)
        self.assertIsNone(manager.current_session)

    def test_start_first_session(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        session = manager.start_session("タスク1")

        self.assertEqual(len(manager.sessions), 1)
        self.assertEqual(manager.current_session, session)
        self.assertEqual(session.task_name, "タスク1")
        self.assertTrue(session.is_running)

    def test_start_second_session_stops_first(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        session1 = manager.start_session("タスク1")
        time.sleep(0.01)
        session2 = manager.start_session("タスク2")

        self.assertEqual(len(manager.sessions), 2)
        self.assertEqual(manager.current_session, session2)
        self.assertFalse(session1.is_running)
        self.assertTrue(session2.is_running)
        self.assertIsNotNone(session1.end_time)

    def test_session_history_preserved(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        session1 = manager.start_session("タスク1")
        time.sleep(0.01)
        session2 = manager.start_session("タスク2")
        time.sleep(0.01)
        session3 = manager.start_session("タスク3")

        self.assertEqual(len(manager.sessions), 3)
        self.assertEqual(manager.sessions[0], session1)
        self.assertEqual(manager.sessions[1], session2)
        self.assertEqual(manager.sessions[2], session3)
        self.assertEqual(manager.current_session, session3)

        self.assertFalse(session1.is_running)
        self.assertFalse(session2.is_running)
        self.assertTrue(session3.is_running)

    def test_get_all_sessions(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        manager.start_session("タスク1")
        manager.start_session("タスク2")
        manager.start_session("タスク3")

        all_sessions = manager.get_all_sessions()
        self.assertEqual(len(all_sessions), 3)
        self.assertEqual(all_sessions[0].task_name, "タスク1")
        self.assertEqual(all_sessions[1].task_name, "タスク2")
        self.assertEqual(all_sessions[2].task_name, "タスク3")

    def test_get_completed_sessions(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        manager.start_session("タスク1")
        manager.start_session("タスク2")
        manager.start_session("タスク3")

        completed = manager.get_completed_sessions()
        self.assertEqual(len(completed), 2)
        self.assertEqual(completed[0].task_name, "タスク1")
        self.assertEqual(completed[1].task_name, "タスク2")
        for session in completed:
            self.assertFalse(session.is_running)
            self.assertIsNotNone(session.end_time)

    def test_stop_current_session(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        session = manager.start_session("タスク1")
        manager.stop_current_session()

        self.assertFalse(session.is_running)
        self.assertIsNotNone(session.end_time)
        self.assertIsNone(manager.current_session)

    def test_stop_current_session_when_none_running(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        manager.stop_current_session()

        self.assertEqual(len(manager.sessions), 0)
        self.assertIsNone(manager.current_session)

    def test_total_time_calculation(self):
        from src.session_manager import SessionManager

        manager = SessionManager()
        manager.start_session("タスク1")
        time.sleep(0.1)
        manager.start_session("タスク2")
        time.sleep(0.1)
        manager.stop_current_session()

        total_time = manager.get_total_time()
        self.assertGreaterEqual(total_time, 0.2)
        self.assertLess(total_time, 1.0)


if __name__ == "__main__":
    unittest.main()