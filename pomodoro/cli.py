"""Simple command-line interface for PomodoroTimer."""
import argparse
import time
from .timer import PomodoroTimer, PomodoroConfig, Phase


def format_time(seconds: int) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02d}:{s:02d}"


def run_timer(config: PomodoroConfig) -> None:
    timer = PomodoroTimer(config)
    timer.start()
    try:
        while True:
            print(f"{timer.current_phase().name}: {format_time(timer.remaining)}", end="\r")
            time.sleep(1)
            timer.tick(1)
    except KeyboardInterrupt:
        print("\nTimer stopped")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Pomodoro timer")
    parser.add_argument("--work", type=int, default=25, help="work minutes")
    parser.add_argument("--short", type=int, default=5, help="short break minutes")
    parser.add_argument("--long", type=int, default=15, help="long break minutes")
    parser.add_argument("--cycles", type=int, default=4, help="cycles before long break")
    parser.add_argument("--manual", action="store_true", help="disable auto transitions")
    args = parser.parse_args()

    config = PomodoroConfig(
        work_minutes=args.work,
        short_break_minutes=args.short,
        long_break_minutes=args.long,
        cycles_before_long_break=args.cycles,
        auto_transition=not args.manual,
    )
    run_timer(config)


if __name__ == "__main__":
    main()
