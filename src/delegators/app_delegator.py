from __future__ import annotations
from src.facades.config.config_reader import ConfigReader
from src.generators.image_generator import ImageGenerator
from src.generators.number_generator import NumberGenerator
from libs.python_library.argument_parser import ArgumentParser


class AppDelegator:
    def __init__(self) -> None:
        pass

    def apply_config(self) -> AppDelegator:
        for key, value in ConfigReader.read().items():
            setattr(self, f'_{key}', value)
            print('[%s]: %s' % (key, value))
        return self
    
    def apply_arguments(self) -> AppDelegator:
        for key, value in ArgumentParser.get_pairs(remove_prefix=True).items():
            setattr(self, f'_{key}', value)
            print('[%s]: %s' % (key, value))
        return self

    def generate_pairs(self) -> AppDelegator:
        print('In generate_pairs')
        self.imgs = {}
        while(len(self.imgs) < self._img_cnt):
            self.imgs[NumberGenerator.generate({
                'config': self._img_config,
                'folder': self._img_folder
            })] = len(self.imgs)
        self.sounds = {}
        while(len(self.sounds) < self._img_cnt):
            self.sounds[NumberGenerator.generate({
                'config': self._sound_config,
                'folder': self._sound_folder
            })]
        return self

    def generate_pictures(self) -> AppDelegator:
        print('In generate_pictures')
        for img_code, index in self.imgs.items():
            ImageGenerator() \
                .decode(img_code) \
                .generate() \
                .show() \
                .save(path=self._output_path)
            print(f'done for image #{index}')
        return self

    def generate_sounds(self) -> AppDelegator:
        print('In generate_sounds')
        return self
    
    def mix_gifs(self) -> AppDelegator:
        return self
