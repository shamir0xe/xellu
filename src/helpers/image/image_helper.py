import numpy as np
from PIL import Image, ImageDraw, ImageFont
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
        return Image.open(PathHelper.from_root(*paths)).convert("RGBA")
    
    @staticmethod
    def rgb_array(image: Image):
        return np.array(image)
    
    @staticmethod
    def text_image(
        string: str, 
        size: tuple[int, int], 
        position: tuple = (0, 0), 
        font_path: str = None,
        font_size: int = 40
    ) -> Image:
        print(f'size: {size}, position: {position}, font_path: {font_path}')
        image = Image.new("RGBA", size, (255, 255, 255, 0))
        font = ImageFont.truetype(font_path, font_size)
        drawing_context = ImageDraw.Draw(image)
        drawing_context.multiline_text(position, string, font=font, fill=(0, 0, 0))
        return image

    @staticmethod
    def paste(image: Image, second_image: Image) -> Image:
        image.paste(second_image, (0, 0), second_image)
        return image
    