from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod

from TrafficLight import LightColor

OFF_COLOR = "#404040"

LAMP_COLORS: dict[LightColor, str] = {
    LightColor.RED: "#ff0000",
    LightColor.RED_AMBER: "#ff8c00",
    LightColor.GREEN: "#00cc00",
    LightColor.AMBER: "#ffbf00",
}

# Lamps lit for each color; RED_AMBER lights the red and amber lamps together.
LIT_LAMPS: dict[LightColor, tuple[LightColor, ...]] = {
    LightColor.RED: (LightColor.RED,),
    LightColor.RED_AMBER: (LightColor.RED, LightColor.AMBER),
    LightColor.GREEN: (LightColor.GREEN,),
    LightColor.AMBER: (LightColor.AMBER,),
}


class ITrafficLightDriver(ABC):
    """Interface for a traffic light shown in the GUI."""

    @abstractmethod
    def activate(self, color: LightColor) -> None:
        ...

    @abstractmethod
    def deactivate(self, color: LightColor) -> None:
        ...

    @abstractmethod
    def deactivateAll(self) -> None:
        ...


class TrafficLightGuiDriver(ITrafficLightDriver):
    def __init__(self, canvas: tk.Canvas, lamp_items: dict[LightColor, int]) -> None:
        self._canvas = canvas
        self._lamp_items = lamp_items

    # Call deactivateAll() first, otherwise circles from the previous color stay lit.
    def activate(self, color: LightColor) -> None:
        for lamp in LIT_LAMPS[color]:
            self._canvas.itemconfig(self._lamp_items[lamp], fill=LAMP_COLORS[lamp])

    def deactivate(self, color: LightColor) -> None:
        for lamp in LIT_LAMPS[color]:
            self._canvas.itemconfig(self._lamp_items[lamp], fill=OFF_COLOR)

    def deactivateAll(self) -> None:
        for item in self._lamp_items.values():
            self._canvas.itemconfig(item, fill=OFF_COLOR)


class TrafficLightConsoleDriver(ITrafficLightDriver):
    def activate(self, color: LightColor) -> None:
        print(color.value)

    def deactivate(self, color: LightColor) -> None:
        pass

    def deactivateAll(self) -> None:
        pass
