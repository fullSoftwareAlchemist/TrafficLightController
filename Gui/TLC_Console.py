from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from TLCFactory import TLCFactory

# Scheduler tick period; phase durations should be multiples of this.
TICK_S = 0.5
# Number of full passes through the sequence to run; None means run forever.
DEBUG_CYCLES: int | None = 2


class TextRedirect:
    """File-like object that writes everything printed into a Text widget."""

    def __init__(self, text: tk.Text) -> None:
        self._text = text

    def write(self, message: str) -> None:
        self._text.insert(tk.END, message)
        self._text.see(tk.END)

    def flush(self) -> None:
        pass


def main() -> None:
    root = tk.Tk()
    root.title("Intersection console")
    text = tk.Text(root, width=60, height=20)
    text.pack(fill=tk.BOTH, expand=True)
    sys.stdout = TextRedirect(text)

    controller = TLCFactory.createConsoleTLC()

    ticks_per_cycle = 20
    ticks_done = 0

    def on_tick() -> None:
        nonlocal ticks_done
        if DEBUG_CYCLES is not None and ticks_done >= DEBUG_CYCLES * ticks_per_cycle:
            return
        controller.tick(TICK_S)
        ticks_done += 1
        root.after(int(TICK_S * 1000), on_tick)

    on_tick()
    root.mainloop()


if __name__ == "__main__":
    main()
