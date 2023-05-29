class TextHelper:
    @staticmethod
    def find_split_index(names: str, split_portion: float) -> int:
        index = int(len(names) * split_portion + 1e-9)
        while index < len(names) and \
            (str.isalpha(names[index]) or names[index] == '\n'):
            index += 1
        return index
