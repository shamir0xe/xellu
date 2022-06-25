from __future__ import annotations
from src.helpers.file.file_finder import FileFinder
from src.helpers.selectors.dict_selector import DictSelector
from src.helpers.data.decoder import Decoder
from src.generators.generator import Generator
from src.helpers.sound.sound_helper import SoundHelper
from src.delegators.sound_delegator import SoundDelegator
from tqdm import tqdm


class SoundGenerator(Generator):
    def __init__(
        self,
        config: dict,
        folder: list,
        basis: int,
        file_type: str
    ) -> None:
        self.config = config["traits"]
        self.folder = folder
        self.basis = basis
        self.file_type = file_type

    def decode(self, code: int) -> SoundGenerator:
        self.code = code
        self.indices = Decoder.decode(code=code, basis=self.basis)
        return self
    
    def unpack_config(self, id: int) -> tuple:
        obj = DictSelector.get_by_id(self.config, id=id)
        instrument = obj[0]
        filters = obj[1]['filters']
        return (instrument, filters)

    def generate(self) -> SoundGenerator:
        print('generating song')
        self.sound = None
        for i, index in enumerate(tqdm(self.indices)):
            if index == 0:
                # it's not selected
                continue
            instrument, filters = self.unpack_config(id=i + 1)
            sound_list = FileFinder.all_files_recursive(*self.folder, instrument, file_type=self.file_type)
            self.sound = SoundDelegator() \
                .load(path=sound_list[index - 1][1], file_type=self.file_type) \
                .apply_filters(filters=filters) \
                .mix(sound=self.sound) \
                .get()
        return self
    
    def mastering(self) -> SoundGenerator:
        self.sound = SoundHelper.mastering_procedure(self.sound)
        return self
    
    def play(self) -> SoundGenerator:
        SoundHelper.play(self.sound)
        return self

    def save(self, path: list) -> SoundGenerator:
        SoundHelper.save(path=[*path, str(self.code) + '.' + self.file_type], sound=self.sound, file_type=self.file_type)
        return self

