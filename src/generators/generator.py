from __future__ import annotations
from abc import ABC


class Generator(ABC):
    def generate(self, *args, **kwargs) -> Generator:
        return self
