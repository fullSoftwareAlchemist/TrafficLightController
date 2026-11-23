# File Access Class Diagram

```mermaid
classDiagram
    class IAccessFiles {
        <<abstract>>
        +read_text() str
    }

    class FileAccess {
        -_path: Path
        +FileAccess(path: Path | str)
        +read_text() str
    }

    class Path {
        <<external: pathlib>>
        +read_text(encoding: str) str
    }

    class TLCConfigProvider {
        <<external: TLCConfigProvider>>
    }

    class TLCFactory {
        <<external: TLCFactory>>
    }

    IAccessFiles <|.. FileAccess : implements
    FileAccess --> Path : holds
    TLCConfigProvider --> IAccessFiles : depends on
    TLCFactory ..> FileAccess : creates
```

`IAccessFiles` and `FileAccess` are defined in `HAL/FileAccess.py`.
`FileAccess` is created with the file path, converts it to `Path`, and
`read_text()` returns the full file content decoded as UTF-8.
`TLCConfigProvider` depends only on `IAccessFiles`, so another implementation
(for example, an in-memory one for tests) can be injected.
