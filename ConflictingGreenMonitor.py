from __future__ import annotations

from abc import ABC, abstractmethod

from HAL.AmmeterAbstraction import IAmmeterGuiDriver, LampState


class IMonitorConflictingGreen(ABC):
    """Interface of a monitor that detects green on main and cross road at the same time."""

    @abstractmethod
    def runMonitor(self) -> bool:
        ...


class ConflictingGreenMonitor(IMonitorConflictingGreen):
    def __init__(self, mainRoad: list[IAmmeterGuiDriver], crossRoad: list[IAmmeterGuiDriver]) -> None:
        self._mainRoad = mainRoad
        self._crossRoad = crossRoad

    def runMonitor(self) -> bool:
        # True means a conflict: at least one green on each road.
        mainGreen = any(ammeter.getGreenState() == LampState.ON for ammeter in self._mainRoad)
        crossGreen = any(ammeter.getGreenState() == LampState.ON for ammeter in self._crossRoad)
        return mainGreen and crossGreen
