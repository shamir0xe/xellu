import os
from pathlib import Path


class PathHelper:
    @staticmethod
    def root_path() -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')

    @staticmethod
    def from_root(*path) -> str:
        return os.path.normpath(os.path.join(PathHelper.root_path(), *path))
