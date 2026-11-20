from __future__ import annotations

from pathlib import Path

from TLC import LeftPhase, Phase
from TrafficLight import LightColor

COLOR_CODES: dict[str, LightColor] = {
    "R": LightColor.RED,
    "RA": LightColor.RED_AMBER,
    "G": LightColor.GREEN,
    "A": LightColor.AMBER,
}


class TLCConfigProvider:
    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)

    def load_sequence(self) -> tuple[Phase | None, ...]:
        phases: list[Phase | None] = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            text = line.strip().rstrip(",")
            if not text or text.startswith("#"):
                continue
            if text == "None":
                phases.append(None)
                continue
            car_main, car_cross, ped_main, ped_cross, duration = (
                field.strip() for field in text.strip("()").split(",")
            )
            phases.append(Phase(
                car_main=COLOR_CODES[car_main],
                car_cross=COLOR_CODES[car_cross],
                ped_main=COLOR_CODES[ped_main],
                ped_cross=COLOR_CODES[ped_cross],
                duration_s=float(duration),
            ))
        return tuple(phases)

    def load_sequenceLeftTurn(self) -> tuple[LeftPhase | None, ...]:
        phases: list[LeftPhase | None] = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            text = line.strip().rstrip(",")
            if not text or text.startswith("#"):
                continue
            if text == "None":
                phases.append(None)
                continue
            car_main, car_cross, ped_main, ped_cross, left_main, left_cross, duration = (
                field.strip() for field in text.strip("()").split(",")
            )
            phases.append(LeftPhase(
                car_main=COLOR_CODES[car_main],
                car_cross=COLOR_CODES[car_cross],
                ped_main=COLOR_CODES[ped_main],
                ped_cross=COLOR_CODES[ped_cross],
                left_main=COLOR_CODES[left_main],
                left_cross=COLOR_CODES[left_cross],
                duration_s=float(duration),
            ))
        return tuple(phases)
