# Conflicting Green Monitor Class Diagram

```mermaid
classDiagram
    class IMonitorConflictingGreen {
        <<abstract>>
        +runMonitor() bool
    }

    class ConflictingGreenMonitor {
        -_mainRoad: list~IAmmeterGuiDriver~
        -_crossRoad: list~IAmmeterGuiDriver~
        +ConflictingGreenMonitor(mainRoad: list~IAmmeterGuiDriver~, crossRoad: list~IAmmeterGuiDriver~)
        +runMonitor() bool
    }

    class IAmmeterGuiDriver {
        <<external interface>>
        +getGreenState() LampState
    }

    class LampState {
        <<enumeration>>
        ON
        OFF
    }

    IMonitorConflictingGreen <|.. ConflictingGreenMonitor : implements
    ConflictingGreenMonitor o-- "*" IAmmeterGuiDriver : mainRoad / crossRoad
    ConflictingGreenMonitor ..> LampState : compares
```

`IAmmeterGuiDriver` and `LampState` are imported from `AmmeterAbstraction.py`.
`runMonitor()` returns `True` (conflict) when at least one ammeter on the main
road and at least one on the cross road report `LampState.ON`.
