from pydub import AudioSegment
from src.helpers.file.path_helper import PathHelper


class SoundHelper:
    @staticmethod
    def load(path: str, file_type: str) -> AudioSegment:
        return AudioSegment.from_file(path, format=file_type)
    
    @staticmethod
    def mix(sound1: AudioSegment, sound2: AudioSegment) -> AudioSegment:
        return sound1.overlay(sound2)
    
    @staticmethod
    def play(sound: AudioSegment) -> None:
        from pydub.playback import play
        play(sound)
    
    @staticmethod
    def save(sound: AudioSegment, file_type: str, path: list) -> None:
        print(f'saving audio to {path}')
        sound.export(PathHelper.from_root(*path), format=file_type)
