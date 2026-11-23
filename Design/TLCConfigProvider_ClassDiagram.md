# TLC Config Provider Class Diagram

```mermaid
classDiagram
    class TLCConfigProvider {
        -_file_access: IAccessFiles
        +TLCConfigProvider(file_access: IAccessFiles)
        +load_sequence() tuple~Phase | None~
        +load_sequenceLeftTurn() tuple~LeftPhase | None~
    }

    class IAccessFiles {
        <<abstract>>
        +read_text() str
    }

    class FileAccess {
        <<external: HAL.FileAccess>>
        +FileAccess(path: Path | str)
        +read_text() str
    }

    class Phase {
        <<external: TLC>>
    }

    class LeftPhase {
        <<external: TLC>>
    }

    class LightColor {
        <<enumeration>>
    }

    class ConfigFiles {
        <<text files in config/>>
        TLCConfig.txt
        TLCLeftConfig.txt
        TLCLeftConfig_hacked.txt
    }

    TLCConfigProvider ..> Phase : creates
    TLCConfigProvider ..> LeftPhase : creates
    TLCConfigProvider ..> LightColor : maps color codes
    TLCConfigProvider --> IAccessFiles : reads through
    IAccessFiles <|.. FileAccess : implements
    FileAccess --> ConfigFiles : reads
```

`Phase` and `LeftPhase` are imported from `TLC.py`; `LightColor` is imported
from `TrafficLight.py`; `IAccessFiles` is imported from `HAL/FileAccess.py`.
Both load methods parse the text returned by the injected `IAccessFiles`, so the
provider does not know file paths. See `FileAccess_ClassDiagram.md`.
