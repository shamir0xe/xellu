import os
import json
from typing import Any
from libs.python_library.helpers.json_helper import JsonHelper
from libs.python_library.io.buffer_reader import BufferReader
from libs.python_library.io.file_buffer import FileBuffer


class ConfigReader:
    def __init__(self, sub_path: str = '', path: list = ['config', 'config.json']) -> None:
        self.sub_path = sub_path
        if sub_path != '':
            self.sub_path = sub_path + '.'
        self.json = read_json(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', *path)))
    
    def get(self, selector: str = '', default: Any = None) -> Any:
        value = JsonHelper.selector_get_value(self.json, self.sub_path + selector)
        if value != {}:
            return value
        return default
    
    @staticmethod
    def read(path: list = ['config', 'config.json'], *args, **kwargs) -> Any:
        return ConfigReader(path=path).get(*args, **kwargs)

def read_json(path: str) -> Any:
    reader = BufferReader(FileBuffer(path))
    data = ''
    while not reader.end_of_buffer():
        data += reader.next_line()
    return json.loads(data)
