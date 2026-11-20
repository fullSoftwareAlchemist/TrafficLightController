from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from enum import Enum

from TrafficLight import LightColor
from TrafficLightAbstraction import LAMP_COLORS


class LampState(Enum):
    ON = "On"
    OFF = "Off"


class IAmmeterGuiDriver(ABC):
    """Interface for reading lamp states of a traffic light shown in the GUI."""

    @abstractmethod
    def getGreenState(self) -> LampState:
        ...


class AmmeterGuiDriver(IAmmeterGuiDriver):
    def __init__(self, canvas: tk.Canvas, lamp_items: dict[LightColor, int]) -> None:
        self._canvas = canvas
        self._lamp_items = lamp_items

    def getGreenState(self) -> LampState:
        fill = self._canvas.itemcget(self._lamp_items[LightColor.GREEN], "fill")
        return LampState.ON if fill == LAMP_COLORS[LightColor.GREEN] else LampState.OFF
