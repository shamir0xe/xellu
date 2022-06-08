from __future__ import annotations
from src.helpers.file.file_finder import FileFinder
from src.helpers.selectors.dict_selector import DictSelector
from src.helpers.data.decoder import Decoder
from src.generators.generator import Generator
from src.helpers.sound.sound_helper import SoundHelper


class SoundGenerator(Generator):
    def __init__(
        self,
        config: dict,
        folder: list,
        basis: int,
        file_type: str
    ) -> None:
        self.config = config
        self.folder = folder
        self.basis = basis
        self.file_type = file_type

    def decode(self, code: int) -> SoundGenerator:
        self.code = code
        self.indices = Decoder.decode(code=code, basis=self.basis)
        return self
    
    def generate(self) -> SoundGenerator:
        self.sound = None
        for i, index in enumerate(self.indices):
            if index == 0:
                # it's not selected
                continue
            obj = DictSelector.get_by_id(self.config, id=i + 1)
            sound_list = FileFinder.all_files_recursive(*self.folder, obj[0], file_type=self.file_type)
            current_sound = SoundHelper.load(sound_list[index - 1][1], file_type=self.file_type)
            if self.sound is None:
                self.sound = current_sound
            else:
                self.sound = SoundHelper.mix(self.sound, current_sound)
        return self
    
    def play(self) -> SoundGenerator:
        SoundHelper.play(self.sound)
        return self

    def save(self, path: list) -> SoundGenerator:
        SoundHelper.save(path=[*path, str(self.code) + '.' + self.file_type], sound=self.sound, file_type=self.file_type)
        return self

