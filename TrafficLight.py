from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Type hints only; avoids a circular import at runtime.
    from TrafficLightAbstraction import ITrafficLightDriver


class LightColor(Enum):
    RED = "Red"
    RED_AMBER = "RedAmber"
    GREEN = "Green"
    AMBER = "Amber"
    OFF = "Off"

class ITrafficLight(ABC):
    """Interface of the traffic light state machine."""

    @abstractmethod
    def setState(self, state: LightColor | str) -> None:
        ...

    @abstractmethod
    def execute(self) -> None:
        ...

class TrafficLight(ITrafficLight):
    def __init__(self, states: dict[LightColor, ITrafficLightState], initial_state: LightColor = LightColor.RED) -> None:
        self._states: dict[LightColor, ITrafficLightState] = states
        self._state: ITrafficLightState = self._states[initial_state]

    @property
    def state(self) -> ITrafficLightState:
        return self._state

    def setState(self, state: LightColor | str) -> None:
        # Raises ValueError for unknown strings, e.g. "Blue".
        self._state = self._states[LightColor(state)]

    def execute(self) -> None:
        self._state.execute()

class ITrafficLightState(ABC):
    """Interface for a single traffic light state."""

    @abstractmethod
    def execute(self) -> None:
        ...

class TrafficLightState(ITrafficLightState):
    """Partial implementation shared by all traffic light states."""

    color: LightColor

    def __init__(self, trafficLightDriver: ITrafficLightDriver) -> None:
        self._trafficLightDriver = trafficLightDriver
    
    def execute(self) -> None:
        self._trafficLightDriver.deactivateAll()
        self._trafficLightDriver.activate(self.color)


class RedState(TrafficLightState):
    color = LightColor.RED


class RedAmberState(TrafficLightState):
    color = LightColor.RED_AMBER


class GreenState(TrafficLightState):
    color = LightColor.GREEN


class AmberState(TrafficLightState):
    color = LightColor.AMBER


class OffState(TrafficLightState):
    color = LightColor.OFF

    def execute(self) -> None:
        self._trafficLightDriver.deactivateAll()
