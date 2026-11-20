# Traffic Light Driver Class Diagram

```mermaid
classDiagram
    class ITrafficLightDriver {
        <<abstract>>
        +activate(color: LightColor) None
        +deactivate(color: LightColor) None
        +deactivateAll() None
    }

    class TrafficLightGuiDriver {
        -_canvas: tk.Canvas
        -_lamp_items: dict~LightColor, int~
        +TrafficLightGuiDriver(canvas: tk.Canvas, lamp_items: dict~LightColor, int~)
        +activate(color: LightColor) None
        +deactivate(color: LightColor) None
        +deactivateAll() None
    }

    class TrafficLightConsoleDriver {
        +activate(color: LightColor) None
        +deactivate(color: LightColor) None
        +deactivateAll() None
    }

    class LightColor {
        <<enumeration>>
    }

    class TkCanvas {
        <<external: tkinter>>
        +itemconfig(item: int, options)
    }

    ITrafficLightDriver <|.. TrafficLightGuiDriver : implements
    ITrafficLightDriver <|.. TrafficLightConsoleDriver : implements
    TrafficLightGuiDriver --> TkCanvas : holds
    TrafficLightGuiDriver ..> LightColor : uses
    TrafficLightConsoleDriver ..> LightColor : prints value
```

`LightColor` is imported from `TrafficLight.py`. The module-level `LIT_LAMPS`,
`LAMP_COLORS`, and `OFF_COLOR` constants determine which lamp items are lit and
which fill colors are applied. `TrafficLightConsoleDriver.activate()` prints the
color value; `deactivate()` and `deactivateAll()` do nothing.
