from __future__ import annotations
import pillow_avif
import re
from src.helpers.file.file_finder import FileFinder
from src.generators.generator import Generator
from src.helpers.data.decoder import Decoder
from src.helpers.selectors.dict_selector import DictSelector
from src.helpers.image.image_helper import ImageHelper
from src.helpers.data.data_transfer_object import DataTransferObject
from src.helpers.file.path_helper import PathHelper
from tqdm import tqdm


class ImageGenerator(Generator):
    def __init__(
        self,
        config: dict,
        folder: list,
        basis: int,
        file_type: str
    ) -> None:
        self.config = DataTransferObject.from_dict(config)
        self.folder = folder
        self.basis = basis
        self.file_type = file_type
        self.name = ''

    def decode(self, code: int) -> ImageGenerator:
        self.code = code
        self.indices = Decoder.decode(basis=self.basis, code=code)
        return self

    def generate(self) -> ImageGenerator:
        print('generating imgae')
        self.image = None
        for i, index in enumerate(tqdm(self.indices)):
            if index == 0:
                # it's not selected
                continue
            category, obj = DictSelector.get_by_id(self.config.traits, id=i + 1)
            obj = DataTransferObject.from_dict(obj)
            image_list = FileFinder.all_files_recursive(*self.folder, category, file_type=self.file_type)
            current_image = ImageHelper.open(image_list[index - 1][1])
            name = obj.names[(index - 1) % len(obj.names)]
            self.name += f' {name}'
            if self.image is None:
                self.image = current_image
            else:
                self.image = ImageHelper.paste(self.image, current_image)
        return self
    
    def add_name(self) -> ImageGenerator:
        print(f'generated name is: {self.name}')
        # make the name vertical
        self.name = '\n'.join([char for char in self.name])
        # print the word on a transparent sheet
        word_image = ImageHelper.text_image(
            self.name, 
            self.image._size, 
            tuple(self.config.names['position']),
            PathHelper.from_root(*self.config.names['font_path']),
            self.config.names['font_size']
        )
        # paste the created image on the main image
        self.image = ImageHelper.paste(self.image, word_image)
        return self
    
    def add_border(self) -> ImageGenerator:
        return self
    
    def show(self) -> ImageGenerator:
        ImageHelper.show(self.image)
        return self

    def save(self, path: list) -> ImageGenerator:
        ImageHelper.save(self.image, *path, str(self.code) + '.' + self.file_type)
        return self
