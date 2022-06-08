from __future__ import annotations
from src.helpers.selectors.dict_selector import DictSelector
from src.facades.config.config_reader import ConfigReader
from src.generators.image_generator import ImageGenerator
from src.generators.sound_generator import SoundGenerator
from src.generators.number_generator import NumberGenerator
from src.generators.mp4_generator import Mp4Generator
from libs.python_library.argument_parser import ArgumentParser


class AppDelegator:
    def __init__(self) -> None:
        pass

    def apply_config(self) -> AppDelegator:
        for key, value in ConfigReader.read().items():
            setattr(self, f'_{key}', value)
            print('[%s]: %s' % (key, value))
        self._img_config = ConfigReader.read(path=self._img_config_path)
        self._sound_config = ConfigReader.read(path=self._sound_config_path)
        return self
    
    def apply_arguments(self) -> AppDelegator:
        for key, value in ArgumentParser.get_pairs(remove_prefix=True).items():
            setattr(self, f'_{key}', int(value))
            print('[%s]: %s' % (key, value))
        return self

    def generate_pairs(self) -> AppDelegator:
        print('In generate_pairs')
        self.imgs = {}
        while(len(self.imgs) < self._img_cnt):
            self.imgs[NumberGenerator(
                config=self._img_config,
                folder=self._img_folder,
                basis=self._max_imgs,
                file_type=self._img_type
            ).generate().output()] = len(self.imgs)
        print('going for sound')
        self.sounds = {}
        while(len(self.sounds) < self._img_cnt):
            self.sounds[NumberGenerator(
                config=self._sound_config,
                folder=self._sound_folder,
                basis=self._max_imgs,
                file_type=self._sound_type
            ).generate().output()] = len(self.sounds)
        return self

    def generate_pictures(self) -> AppDelegator:
        print('In generate_pictures')
        for img_code, index in self.imgs.items():
            print(f'image #{index} = {img_code}')
            ImageGenerator(
                config=self._img_config,
                folder=self._img_folder,
                basis=self._max_imgs,
                file_type=self._img_type
            ) \
                .decode(img_code) \
                .generate() \
                .save(path=self._output_path['imgs'])
            print(f'done for image #{index}')
        return self

    def generate_sounds(self) -> AppDelegator:
        print('In generate_sounds')
        for sound_code, index in self.sounds.items():
            print(f'sound #{index} = {sound_code}')
            SoundGenerator(
                config=self._sound_config,
                folder=self._sound_folder,
                basis=self._max_imgs,
                file_type=self._sound_type
            ) \
                .decode(sound_code) \
                .generate() \
                .save(path=self._output_path['sounds'])
            print(f'done music for #{index}')
        return self
    
    def mix(self) -> AppDelegator:
        for i in range(self._img_cnt):
            Mp4Generator(
                sound_id=DictSelector.get_by_value(self.sounds, i)[0],
                img_id=DictSelector.get_by_value(self.imgs, i)[0]
            ) \
                .load_img(path=self._output_path['imgs'], file_type=self._img_type) \
                .load_sound(path=self._output_path['sounds'], file_type=self._sound_type) \
                .generate() \
                .save(path=self._output_path['mp4s'])
        return self
