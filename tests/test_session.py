import unittest
import time
from datetime import datetime
from unittest.mock import patch


class TestSession(unittest.TestCase):
    def test_session_creation(self):
        from src.session import Session

        session = Session("テストタスク")
        self.assertEqual(session.task_name, "テストタスク")
        self.assertIsNone(session.start_time)
        self.assertIsNone(session.end_time)
        self.assertFalse(session.is_running)

    def test_session_start(self):
        from src.session import Session

        session = Session("テストタスク")
        start_time = datetime.now()
        session.start()

        self.assertIsNotNone(session.start_time)
        self.assertTrue(session.is_running)
        self.assertIsNone(session.end_time)
        self.assertGreaterEqual(session.start_time, start_time)

    def test_session_stop(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        time.sleep(0.01)
        session.stop()

        self.assertIsNotNone(session.start_time)
        self.assertIsNotNone(session.end_time)
        self.assertFalse(session.is_running)
        self.assertGreater(session.end_time, session.start_time)

    def test_session_duration(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        time.sleep(0.1)
        session.stop()

        duration = session.get_duration()
        self.assertGreaterEqual(duration, 0.1)
        self.assertLess(duration, 1.0)

    def test_session_duration_while_running(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        time.sleep(0.05)

        duration = session.get_duration()
        self.assertGreaterEqual(duration, 0.05)
        self.assertLess(duration, 1.0)

    def test_session_cannot_start_twice(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()

        with self.assertRaises(ValueError):
            session.start()

    def test_session_cannot_stop_before_start(self):
        from src.session import Session

        session = Session("テストタスク")

        with self.assertRaises(ValueError):
            session.stop()

    def test_session_duration_format(self):
        from src.session import Session

        session = Session("テストタスク")
        with patch.object(session, "get_duration", return_value=3661.5):
            formatted = session.format_duration()
            self.assertEqual(formatted, "01:01:01")

    def test_session_str_representation(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        session.stop()

        str_repr = str(session)
        self.assertIn("テストタスク", str_repr)
        self.assertIn(":", str_repr)

    def test_pause_running_session(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        self.assertTrue(session.is_running)
        self.assertFalse(session.is_paused)

        session.pause()
        self.assertTrue(session.is_running)
        self.assertTrue(session.is_paused)

    def test_pause_not_running_session_raises_error(self):
        from src.session import Session

        session = Session("テストタスク")
        with self.assertRaises(ValueError):
            session.pause()

    def test_resume_paused_session(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        session.pause()
        self.assertTrue(session.is_paused)

        session.resume()
        self.assertTrue(session.is_running)
        self.assertFalse(session.is_paused)

    def test_resume_not_paused_session_raises_error(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        with self.assertRaises(ValueError):
            session.resume()

    def test_paused_time_not_counted_in_duration(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        time.sleep(0.1)
        session.pause()
        initial_duration = session.get_duration()

        time.sleep(0.1)
        paused_duration = session.get_duration()
        self.assertAlmostEqual(initial_duration, paused_duration, delta=0.01)

    def test_duration_continues_after_resume(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        time.sleep(0.1)
        session.pause()
        pause_duration = session.get_duration()

        session.resume()
        time.sleep(0.1)
        resume_duration = session.get_duration()

        self.assertGreater(resume_duration, pause_duration)
        self.assertGreaterEqual(resume_duration, 0.2)

    def test_stop_paused_session(self):
        from src.session import Session

        session = Session("テストタスク")
        session.start()
        session.pause()
        session.stop()

        self.assertFalse(session.is_running)
        self.assertFalse(session.is_paused)
        self.assertIsNotNone(session.end_time)


if __name__ == "__main__":
    unittest.main()
