# Ammeter Abstraction Class Diagram

```mermaid
classDiagram
    class LampState {
        <<enumeration>>
        ON
        OFF
    }

    class IAmmeterGuiDriver {
        <<abstract>>
        +getGreenState() LampState
    }

    class AmmeterGuiDriver {
        -_canvas: tk.Canvas
        -_lamp_items: dict~LightColor, int~
        +AmmeterGuiDriver(canvas: tk.Canvas, lamp_items: dict~LightColor, int~)
        +getGreenState() LampState
    }

    class LightColor {
        <<enumeration>>
    }

    class TkCanvas {
        <<external: tkinter>>
        +itemcget(item: int, option: str) str
    }

    IAmmeterGuiDriver <|.. AmmeterGuiDriver : implements
    IAmmeterGuiDriver ..> LampState : returns
    AmmeterGuiDriver --> TkCanvas : reads lamp fill
    AmmeterGuiDriver ..> LightColor : uses
```

`LightColor` is imported from `TrafficLight.py` and `LAMP_COLORS` from
`TrafficLightAbstraction.py`. `getGreenState()` returns `ON` when the green
lamp's fill equals `LAMP_COLORS[LightColor.GREEN]`, otherwise `OFF`.
