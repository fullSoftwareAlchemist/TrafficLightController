# Lets type hints like tuple[Phase, ...] be used on older Python versions.
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from TrafficLight import ITrafficLight, LightColor


# Frozen: a Phase cannot be changed after it is created.
@dataclass(frozen=True)
class Phase:
    """One row of the intersection sequence table."""

    car_main: LightColor
    car_cross: LightColor
    ped_main: LightColor
    ped_cross: LightColor
    duration_s: float


# Frozen subclasses must be frozen too.
@dataclass(frozen=True)
class LeftPhase(Phase):
    left_main: LightColor = LightColor.RED
    left_cross: LightColor = LightColor.RED


class ITLCState(ABC):
    """Interface of the controller that advances the traffic light sequence."""

    @abstractmethod
    def tick(self, elapsed_s: float) -> None:
        ...

class TlcNormalOperationState(ITLCState):
    def __init__(self, sequence: tuple[Phase | None, ...], traffic_lights: dict[str, ITrafficLight]) -> None:
        if all(phase is None for phase in sequence):
            raise ValueError("sequence needs at least one Phase")
        self._sequence = sequence
        self._current_phase_index = 0
        self._seconds_left_in_phase = 0.0
        # Keyed by Phase field name, e.g. "car_main".
        self._traffic_lights = traffic_lights

    def tick(self, elapsed_s: float) -> None:
        # Called by the scheduler every elapsed_s seconds.
        if self._seconds_left_in_phase <= 0:
            phase_index, phase = self._next_real_phase()
            self._display_phase(phase_index, phase)
            self._seconds_left_in_phase = phase.duration_s
        self._seconds_left_in_phase -= elapsed_s

    def _next_real_phase(self) -> tuple[int, Phase]:
        # Skips None placeholders so they take no time.
        while True:
            index = self._current_phase_index
            phase = self._sequence[index]
            self._current_phase_index = (index + 1) % len(self._sequence)
            if phase is not None:
                return index, phase

    def _display_phase(self, phase_index: int, phase: Phase) -> None:
        print(f"--- Phase {phase_index + 1}/{len(self._sequence)} ({phase.duration_s}s) ---")
        for name, light in self._traffic_lights.items():
            # getattr reads the field with this name, e.g. phase.car_main.
            light.setState(getattr(phase, name))
            light.execute()


class TlcSafeState(TlcNormalOperationState):
    def __init__(self, traffic_lights: dict[str, ITrafficLight]) -> None:
        sequence = (
            LeftPhase(LightColor.AMBER, LightColor.AMBER, LightColor.OFF, LightColor.OFF, 1.0,
                      left_main=LightColor.AMBER, left_cross=LightColor.AMBER),
            LeftPhase(LightColor.OFF, LightColor.OFF, LightColor.OFF, LightColor.OFF, 1.0,
                      left_main=LightColor.OFF, left_cross=LightColor.OFF),
        )
        super().__init__(sequence, traffic_lights)



class ITrafficLightController(ABC):
    """Interface of a controller that can enter a safe state."""

    @abstractmethod
    def tick(self, elapsed_s: float) -> None:
        ...

    @abstractmethod
    def EnterSafeState(self) -> None:
        ...


class TrafficLightController(ITrafficLightController):
    def __init__(self, state: ITLCState, safe_state: TlcSafeState) -> None:
        self._state = state
        self._safe_state = safe_state

    def EnterSafeState(self) -> None:
        self._state = self._safe_state

    def tick(self, elapsed_s: float) -> None:
        self._state.tick(elapsed_s)
