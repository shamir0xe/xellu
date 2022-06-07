from __future__ import annotations
from src.generators.generator import Generator


class SoundGenerator(Generator):
    def __init__(self) -> None:
        pass

    def decode(self, sound_code: int) -> SoundGenerator:
        return self
    
    def save(self, path: list) -> SoundGenerator:
        return self

    def generate(self) -> SoundGenerator:
        return self
