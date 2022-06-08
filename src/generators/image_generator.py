from __future__ import annotations
from PIL import Image
from src.helpers.file.file_finder import FileFinder
from src.generators.generator import Generator
from src.helpers.data.decoder import Decoder
from src.helpers.selectors.dict_selector import DictSelector
from src.helpers.image.image_helper import ImageHelper


class ImageGenerator(Generator):
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

    def decode(self, code: int) -> ImageGenerator:
        self.code = code
        self.indices = Decoder.decode(basis=self.basis, code=code)
        return self

    def generate(self) -> ImageGenerator:
        self.image = None
        for i, index in enumerate(self.indices):
            if index == 0:
                # it's not selected
                continue
            obj = DictSelector.get_by_id(self.config, id=i + 1)
            image_list = FileFinder.all_files_recursive(*self.folder, obj[0], file_type=self.file_type)
            current_image = ImageHelper.open(image_list[index - 1][1])
            if self.image is None:
                self.image = current_image
            else:
                self.image = ImageHelper.paste(self.image, current_image)
        return self
    
    def show(self) -> ImageGenerator:
        ImageHelper.show(self.image)
        return self

    def save(self, path: list) -> ImageGenerator:
        ImageHelper.save(self.image, *path, str(self.code) + '.' + self.file_type)
        return self
