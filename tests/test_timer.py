import unittest
from pomodoro.timer import PomodoroTimer, PomodoroConfig, Phase


class TestPomodoroTimer(unittest.TestCase):
    def test_auto_transition_cycle(self):
        config = PomodoroConfig(
            work_minutes=1,
            short_break_minutes=1,
            long_break_minutes=2,
            cycles_before_long_break=2,
            auto_transition=True,
        )
        timer = PomodoroTimer(config)
        timer.start()
        timer.tick(60)  # complete focus
        self.assertEqual(timer.current_phase(), Phase.SHORT_BREAK)
        self.assertTrue(timer.is_running())
        timer.tick(60)  # complete short break
        self.assertEqual(timer.current_phase(), Phase.FOCUS)
        timer.tick(60)  # complete second focus -> long break
        self.assertEqual(timer.current_phase(), Phase.LONG_BREAK)
        timer.tick(120)  # complete long break
        self.assertEqual(timer.current_phase(), Phase.FOCUS)

    def test_manual_transition(self):
        config = PomodoroConfig(work_minutes=1, short_break_minutes=1, auto_transition=False)
        timer = PomodoroTimer(config)
        timer.start()
        timer.tick(60)  # complete focus
        self.assertEqual(timer.current_phase(), Phase.SHORT_BREAK)
        self.assertFalse(timer.is_running())
        timer.start()  # manually start break
        self.assertTrue(timer.is_running())


if __name__ == "__main__":
    unittest.main()
