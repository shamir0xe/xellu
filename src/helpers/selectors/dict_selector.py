from typing import Any


class DictSelector:
    @staticmethod
    def get_by_id(obj: dict, id: int) -> tuple:
        temp = list(filter(lambda obj: obj[1]['id'] == id, obj.items()))
        if len(temp) <= 0:
            return None
            raise Exception('invalid id provided')
        return temp[0]
    
    @staticmethod
    def get_by_attribute(dictionary: dict, **kwargs) -> tuple:
        def check(tup: tuple, **kwargs) -> bool:
            for key, value in kwargs:
                if tup[0] == key and tup[1] == value:
                    return True
            return False
        filtered_list = list(filter(lambda temp: check(temp, **kwargs), dictionary.items()))
        if len(filtered_list) <= 0:
            return None
            raise Exception('invalid attributes')
        return filtered_list[0]
    
    @staticmethod
    def get_by_value(dictionary: dict, value: Any) -> tuple:
        filtered_list = list(filter(lambda temp: temp[1] == value, dictionary.items()))
        if len(filtered_list) <= 0:
            return None
            raise Exception('invalid value provided')
        return filtered_list[0]
