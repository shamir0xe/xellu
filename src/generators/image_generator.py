from __future__ import annotations
from src.generators.generator import Generator


class ImageGenerator(Generator):
    def __init__(self) -> None:
        pass

    def decode(self, code: int) -> ImageGenerator:
        return self

    def generate(self) -> ImageGenerator:
        return self
    
    def show(self) -> ImageGenerator:
        return self

    def save(self, path: str) -> ImageGenerator:
        return self