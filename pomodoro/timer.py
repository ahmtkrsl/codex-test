"""Pomodoro timer core service.

Provides epoch-based ticking and session cycling following the Pomodoro technique.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Phase(Enum):
    """Different phases of a Pomodoro cycle."""

    FOCUS = auto()
    SHORT_BREAK = auto()
    LONG_BREAK = auto()


@dataclass
class PomodoroConfig:
    work_minutes: int = 25
    short_break_minutes: int = 5
    long_break_minutes: int = 15
    cycles_before_long_break: int = 4
    auto_transition: bool = True


class PomodoroTimer:
    """A simple timer implementing basic Pomodoro logic.

    The timer is **tick based** – tests can advance time deterministically by
    calling :meth:`tick` instead of waiting in real time.
    """

    def __init__(self, config: PomodoroConfig | None = None):
        self.config = config or PomodoroConfig()
        self.phase: Phase = Phase.FOCUS
        self.state: str = "idle"  # idle | running | paused
        self.remaining: int = self.config.work_minutes * 60
        self._cycle_count: int = 0  # completed focus sessions in current set

    # Public API -----------------------------------------------------------
    def start(self) -> None:
        """Start or resume the current phase."""
        if self.state in {"idle", "paused"}:
            self.state = "running"

    def pause(self) -> None:
        if self.state == "running":
            self.state = "paused"

    def tick(self, seconds: int) -> None:
        """Advance the timer by ``seconds``.

        When ``auto_transition`` is disabled and a phase completes, the timer
        stops with ``state='idle'`` and the next phase is prepared but not
        started until :meth:`start` is called again.
        """
        if self.state != "running":
            return
        self.remaining -= seconds
        while self.remaining <= 0 and self.state == "running":
            self._complete_phase()

    # Internal helpers ----------------------------------------------------
    def _complete_phase(self) -> None:
        """Handle completion of the current phase."""
        overflow = -self.remaining
        if self.phase == Phase.FOCUS:
            self._cycle_count += 1
            if self._cycle_count % self.config.cycles_before_long_break == 0:
                next_phase = Phase.LONG_BREAK
                duration = self.config.long_break_minutes * 60
                self._cycle_count = 0
            else:
                next_phase = Phase.SHORT_BREAK
                duration = self.config.short_break_minutes * 60
        elif self.phase in {Phase.SHORT_BREAK, Phase.LONG_BREAK}:
            next_phase = Phase.FOCUS
            duration = self.config.work_minutes * 60
        else:
            next_phase = Phase.FOCUS
            duration = self.config.work_minutes * 60

        self.phase = next_phase
        self.remaining = duration + overflow  # carry over extra seconds
        if self.config.auto_transition:
            self.state = "running"
        else:
            self.state = "idle"

    def is_running(self) -> bool:
        return self.state == "running"

    def current_phase(self) -> Phase:
        return self.phase

    def reset(self) -> None:
        """Reset timer to initial focus phase."""
        self.phase = Phase.FOCUS
        self.state = "idle"
        self.remaining = self.config.work_minutes * 60
        self._cycle_count = 0
