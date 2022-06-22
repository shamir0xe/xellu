import numpy as np
from PIL import Image
from src.helpers.file.path_helper import PathHelper


class ImageHelper:
    @staticmethod
    def show(image: Image) -> None:
        image.show()
    
    @staticmethod
    def save(image: Image, *paths) -> None:
        print(f'save to : {paths}')
        image.save(PathHelper.from_root(*paths))
    
    @staticmethod
    def open(*paths) -> Image:
        return Image.open(PathHelper.from_root(*paths))
    
    @staticmethod
    def rgb_array(image: Image):
        return np.array(image)

    @staticmethod
    def paste(image: Image, second_image: Image) -> Image:
        image.paste(second_image, (0, 0), second_image)
        return image
    