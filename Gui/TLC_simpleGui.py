from __future__ import annotations

from pathlib import Path
import sys
import tkinter as tk

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from TLCConfigProvider import TLCConfigProvider
from TLCFactory import TLCFactory
from HAL.AmmeterAbstraction import AmmeterGuiDriver
from ConflictingGreenMonitor import ConflictingGreenMonitor
from TrafficLight import LightColor
from HAL.TrafficLightAbstraction import OFF_COLOR, TrafficLightGuiDriver

# Short aliases so the sequence table below is easy to read.
R = LightColor.RED
RA = LightColor.RED_AMBER
G = LightColor.GREEN
A = LightColor.AMBER


# Scheduler tick period; phase durations should be multiples of this.
TICK_S = 0.5

CAR_LAMPS = (LightColor.RED, LightColor.AMBER, LightColor.GREEN)
PEDESTRIAN_LAMPS = (LightColor.RED, LightColor.GREEN)
# Left to right: name, x position, lamps.
LIGHT_LAYOUT = (
    ("car_main", 120, CAR_LAMPS),
    ("ped_main", 200, PEDESTRIAN_LAMPS),
    ("car_cross", 360, CAR_LAMPS),
    ("ped_cross", 440, PEDESTRIAN_LAMPS),
)
CANVAS_WIDTH = 480
CANVAS_HEIGHT = 260
LABEL_Y = 12


def create_lamps(
    canvas: tk.Canvas, x: int, y: int, lamps: tuple[LightColor, ...], radius: int = 30, spacing: int = 70
) -> dict[LightColor, int]:
    lamp_items: dict[LightColor, int] = {}
    for index, lamp in enumerate(lamps):
        lamp_y = y + (index - (len(lamps) - 1) / 2) * spacing
        lamp_items[lamp] = canvas.create_oval(
            x - radius, lamp_y - radius, x + radius, lamp_y + radius,
            fill=OFF_COLOR, outline="black", width=2,
        )
    return lamp_items


def main() -> None:
    root = tk.Tk()
    root.title("Simple Intersection")
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()
    lights: dict[str, TrafficLightGuiDriver] = {}
    ammeters: dict[str, AmmeterGuiDriver] = {}
    for name, x, lamps in LIGHT_LAYOUT:
        lamp_items = create_lamps(canvas, x, CANVAS_HEIGHT // 2, lamps)
        canvas.create_text(x, LABEL_Y, text=name)
        lights[name] = TrafficLightGuiDriver(canvas, lamp_items)
        ammeters[name] = AmmeterGuiDriver(canvas, lamp_items)

    controller = TLCFactory.createGuiTLC(lights)

    error_button = tk.Button(root, text="ERROR", command=controller.EnterSafeState)
    error_button.pack()
    malfunction = False

    def set_malfunction() -> None:
        nonlocal malfunction
        malfunction = True

    malfunction_button = tk.Button(root, text="MALFUNCTION", command=set_malfunction)
    malfunction_button.pack()

    # Create a monitor for conflicting green lights.
    ammeterMainRoad = [ammeters["car_main"], ammeters["ped_main"]]
    ammeterCrossRoad = [ammeters["car_cross"], ammeters["ped_cross"]]
    conflictMonitor = ConflictingGreenMonitor(ammeterMainRoad, ammeterCrossRoad)

    def on_tick() -> None:
        controller.tick(TICK_S)
        if malfunction:
            lights["car_main"].activate(LightColor.GREEN)
        if conflictMonitor.runMonitor():
            controller.EnterSafeState()
        # Reschedule instead of a while loop so tkinter's mainloop stays responsive.
        root.after(int(TICK_S * 1000), on_tick)

    on_tick()
    root.mainloop()


if __name__ == "__main__":
    main()
