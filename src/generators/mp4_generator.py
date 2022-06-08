from __future__ import annotations
from src.generators.generator import Generator
from src.helpers.file.path_helper import PathHelper
from moviepy.editor import AudioFileClip, ImageClip


class Mp4Generator(Generator):
    def __init__(
        self,
        sound_id: int,
        img_id: int
    ) -> None:
        print(f'mixing sound#{sound_id} with img#{img_id}')
        self.sound_id = sound_id
        self.img_id = img_id
    
    def load_img(self, path: list, file_type: str) -> Mp4Generator:
        self.img_clip = ImageClip(PathHelper.from_root(*path, f'{self.img_id}.{file_type}'))
        return self
    
    def load_sound(self, path: list, file_type: str) -> Mp4Generator:
        self.audio_clip = AudioFileClip(PathHelper.from_root(*path, f'{self.sound_id}.{file_type}'))
        return self
    
    def generate(self) -> Mp4Generator:
        self.video_clip = self.img_clip.set_audio(self.audio_clip)
        self.video_clip.duration = self.audio_clip.duration
        self.video_clip.fps = 1
        return self
    
    def save(self, path: list) -> Mp4Generator:
        self.video_clip.write_videofile(PathHelper.from_root(*path, f'{self.sound_id}-{self.img_id}.mp4'))
        return self
