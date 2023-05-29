from __future__ import annotations
from functools import reduce
import random
from src.helpers.datastructures.basis_map import BasisMap
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
        self.file_type = file_type
        self.basis_map = BasisMap(basis=basis)

    def generate(self) -> NumberGenerator:
        self.basis_map.clear()
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
            self.add_trait(id=obj.id, value=index)
        # print(f'list before sort: {temp}')
        temp.sort()
        temp = list(map(lambda x: x[1], temp))
        print(f'created list: {temp}')
        return self
    
    def group_selection(self) -> NumberGenerator:
        groups = self.get_groups()
        # print(f'groups: {groups}')
        if len(groups) <= 1:
            return self
        random_group = random.sample(groups, k=1)[0]
        print(f'selected group: {random_group}')
        for index, value in iter(self.basis_map):
            if value > 0:
                # we have selected this attribute
                # print(f'({index + 1}, {value})')
                group = self.get_group(id=index + 1)
                if group != random_group:
                    # print(f'removing this trait: {index + 1} ~~ {group} != {random_group}')
                    self.remove_trait(id=index + 1)
        return self
    
    def get_groups(self) -> list:
        groups = set()
        for index, value in iter(self.basis_map):
            if value > 0:
                groups.add(self.get_group(id=index + 1))
        return list(groups)

    def get_group(self, id: int) -> int:
        obj = DictSelector.get_by_id(obj=self.config["traits"], id=id)[1]
        return obj["group"] if "group" in obj else 0

    def condition_correcting(self) -> NumberGenerator:
        print('in condition correcting')
        correct = False
        while not correct:
            self.group_selection()
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
                                obj = DictSelector.get_by_id(
                                    obj=self.config["traits"],
                                    id=idx
                                )
                                weights = obj[1]["weights"]
                                attr_name = obj[0]
                                # print('NEW wights to add: ', weights)
                                self.add_trait(
                                    id=idx, 
                                    value=Helper(*self.folder, attr_name) \
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
                                self.remove_trait(id=idx)
            if "must-not-if" in self.config["conditions"]:
                for key, value in self.config["conditions"]["must-not-if"].items():
                    key = int(key)
                    if not self.exists_trait(key):
                        for idx in value:
                            bl = not self.exists_trait(idx)
                            correct &= bl
                            if not bl:
                                print(f'oops we gonna remove index: {idx}')
                                self.remove_trait(id=idx)
        return self

    def exists_trait(self, id: int) -> bool:
        return self.basis_map.get_value(index=id - 1) > 0

    def remove_trait(self, id: int) -> NumberGenerator:
        self.basis_map.remove_index(index=id - 1)
        return self

    def add_trait(self, id: int, value: int) -> NumberGenerator:
        self.basis_map.set_value(index=id - 1, value=value)
        return self
    
    def output(self) -> int:
        return self.basis_map.associated_number()

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
