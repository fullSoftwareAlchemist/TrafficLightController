from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class IAccessFiles(ABC):
    @abstractmethod
    def read_text(self) -> str:
        ...


class FileAccess(IAccessFiles):
    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)

    def read_text(self) -> str:
        return self._path.read_text(encoding="utf-8")