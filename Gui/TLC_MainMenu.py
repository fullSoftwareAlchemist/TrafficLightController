from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk

BASE_DIR = Path(__file__).parent

# Button label, the script that contains the GUI's main(), and extra command-line arguments.
GUI_SCRIPTS = (
    ("Console_Intersection", "TLC_Console.py", ()),
    ("Simple_Intersection", "TLC_simpleGui.py", ()),
    ("Intersection_with_Left_Turn", "TLC_leftTurnGui.py", ()),
    ("Hacked Intersection", "TLC_leftTurnGui.py", ("--hacked",)),
)


def launch(script_name: str, args: tuple[str, ...]) -> None:
    # Separate process so each GUI gets its own Tk root and mainloop.
    subprocess.Popen([sys.executable, str(BASE_DIR / script_name), *args])


def main() -> None:
    root = tk.Tk()
    root.title("TLC Main Menu")
    for label, script_name, args in GUI_SCRIPTS:
        tk.Button(root, text=label, width=30, command=lambda s=script_name, a=args: launch(s, a)).pack(padx=20, pady=5)
    root.mainloop()


if __name__ == "__main__":
    main()
