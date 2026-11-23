# TLC Factory Class Diagram

```mermaid
classDiagram
    class TLCFactory {
        +createTrafficLightStates(trafficLightDriver: ITrafficLightDriver)$ dict~LightColor, ITrafficLightState~
        +createConsoleTLC()$ TrafficLightController
        +createGuiTLC(trafficLightDrivers: dict~str, ITrafficLightDriver~)$ TrafficLightController
        +createGuiLeftTurnTLC(trafficLightDrivers: dict~str, ITrafficLightDriver~)$ TrafficLightController
        +createHackedGuiLeftTurnTLC(trafficLightDrivers: dict~str, ITrafficLightDriver~)$ TrafficLightController
    }

    class TLCConfigProvider {
        +TLCConfigProvider(file_access: IAccessFiles)
        +load_sequence() tuple~Phase | None~
        +load_sequenceLeftTurn() tuple~LeftPhase | None~
    }

    class IAccessFiles {
        <<abstract>>
        +read_text() str
    }

    class FileAccess {
        +FileAccess(path: Path | str)
        +read_text() str
    }

    class TrafficLightController
    class TlcNormalOperationState
    class TlcSafeState
    class TrafficLight
    class TrafficLightState
    class ITrafficLightDriver {
        <<interface>>
    }
    class TrafficLightConsoleDriver

    TLCFactory ..> FileAccess : creates with config file path
    TLCFactory ..> TLCConfigProvider : loads sequences
    TLCConfigProvider --> IAccessFiles : reads through
    IAccessFiles <|.. FileAccess : implements
    TLCFactory ..> TrafficLightController : creates
    TLCFactory ..> TlcNormalOperationState : creates
    TLCFactory ..> TlcSafeState : creates
    TLCFactory ..> TrafficLight : creates
    TLCFactory ..> TrafficLightState : creates Red/RedAmber/Green/Amber/Off states
    TLCFactory ..> ITrafficLightDriver : passes drivers to states
    TLCFactory ..> TrafficLightConsoleDriver : creates for console TLC
    ITrafficLightDriver <|.. TrafficLightConsoleDriver : implements
```

The diagram focuses on the types used directly by the factory methods; sequence
values are omitted. The factory creates a `FileAccess` for `config/TLCConfig.txt`,
`config/TLCLeftConfig.txt`, or `config/TLCLeftConfig_hacked.txt` and injects it
into `TLCConfigProvider`.
