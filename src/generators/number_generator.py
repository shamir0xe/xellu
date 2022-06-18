from __future__ import annotations
from functools import reduce
import random
from src.helpers.data.data_transfer_object import DataTransferObject
from src.generators.generator import Generator
from src.helpers.file.file_finder import FileFinder
from src.helpers.selectors.dict_selector import DictSelector


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
        for key, value in self.config["traits"].items():
            obj = DataTransferObject.from_dict(value)
            index = Helper(*self.folder, key) \
                .get_list(file_type=self.file_type) \
                .extend_probabilities(weights=obj.weights) \
                .check_presence(probability=obj.presence_probability) \
                .find_index() \
                .output()
            temp.append((obj.id, index))
            self.add_trait(index=obj.id, value=index)
            # self.generated_number += (self.basis ** (obj.id - 1)) * index
        # print(f'list before sort: {temp}')
        temp.sort()
        temp = list(map(lambda x: x[1], temp))
        print(f'created list: {temp}')
        return self
    
    def condition_correcting(self) -> NumberGenerator:
        print('in condition correcting')
        correct = False
        while not correct:
            correct = True
            if "must" in self.config["conditions"]:
                for key, value in self.config["conditions"]["must"].items():
                    key = int(key)
                    if self.exists_trait(key):
                        for idx in value:
                            bl = self.exists_trait(idx)
                            correct &= bl
                            if not bl:
                                print(f'oops we gonnad add index: {idx}')
                                weights = DictSelector.get_by_attribute(
                                    dictionary=self.config["traits"].items(),
                                    id=idx
                                )[1]["weights"]
                                print('NEW wights to add: ', weights)
                                self.add_trait(
                                    index=idx, 
                                    value=Helper(*self.folder, key) \
                                        .get_list(file_type=self.file_type) \
                                        .extend_probabilities(weights=weights) \
                                        .find_index() \
                                        .output()
                                )
            if "must-not" in self.config["conditions"]:
                mustnot_list = list(self.config["conditions"]["must-not"].items())
                for key, value in random.sample(mustnot_list, len(mustnot_list)):
                    key = int(key)
                    if self.exists_trait(key):
                        for idx in value:
                            bl = not self.exists_trait(idx)
                            correct &= bl
                            if not bl:
                                print(f'oops we gonna remove index: {idx}')
                                self.remove_trait(index=idx)
        return self

    def index_value(self, index: int) -> int:
        number = self.generated_number
        for _ in range(index - 1):
            number = number // self.basis
        return number % self.basis

    def exists_trait(self, index: int) -> bool:
        return self.index_value(index=index) > 0

    def remove_trait(self, index: int) -> NumberGenerator:
        value = self.index_value(index=index)
        self.generated_number -= self.basis ** (index - 1) * value
        return self

    def add_trait(self, index: int, value: int) -> NumberGenerator:
        self.remove_trait(index=index)
        self.generated_number += self.basis ** (index - 1) * value
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
