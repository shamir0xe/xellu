class DictSelector:
    @staticmethod
    def get_by_id(obj: dict, id: int) -> tuple:
        temp = list(filter(lambda obj: obj[1]['id'] == id, obj.items()))
        if len(temp) <= 0:
            raise Exception('invalid id provided')
        return temp[0]
