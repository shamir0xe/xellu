from __future__ import annotations
from functools import reduce
import random
from src.helpers.data.data_transfer_object import DataTransferObject
from src.generators.generator import Generator
from src.helpers.file.file_finder import FileFinder


class NumberGenerator(Generator):
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

    def generate(self) -> NumberGenerator:
        self.generated_number = 0
        temp = []
        for key, value in self.config.items():
            obj = DataTransferObject.from_dict(value)
            index = Helper(*self.folder, key) \
                .get_list(file_type=self.file_type) \
                .extend_probabilities(weights=obj.weights) \
                .check_presence(probability=obj.presence_probability) \
                .find_index() \
                .output()
            temp.append((obj.id, index))
            self.generated_number += (self.basis ** (obj.id - 1)) * index
        # print(f'list before sort: {temp}')
        temp.sort()
        temp = list(map(lambda x: x[1], temp))
        print(f'created list: {temp}')
        return self
    
    def output(self) -> int:
        return self.generated_number

class Helper:
    def __init__(self, *args) -> None:
        self.index = -1
        self.path = args
        self.valid = True
    
    def get_list(self, file_type: str) -> Helper:
        self.total_list = FileFinder.all_files_recursive(*self.path, file_type=file_type)
        return self
    
    def extend_probabilities(self, weights: list) -> Helper:
        self.weights = weights
        while len(self.weights) < len(self.total_list):
            self.weights.append(self.weights[-1])
        return self
    
    def check_presence(self, probability: float) -> Helper:
        if probability < random.random():
            self.valid = False
        return self

    def find_index(self) -> Helper:
        if not self.valid:
            return self
        total_sum = reduce(lambda a, b: a + b, self.weights)
        random_goal = random.randint(0, total_sum)
        cur = 0
        for index, weight in enumerate(self.weights):
            cur += weight
            if cur >= random_goal:
                self.index = index
                break
        return self

    def output(self) -> int:
        """
        returning 1-based index
        """
        return self.index + 1
