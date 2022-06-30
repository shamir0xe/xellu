from __future__ import annotations


class BasisMap:
    def __init__(self, basis: int, init_value: int=0) -> None:
        self.basis: int = basis
        self.number: int = init_value
    
    def set_value(self, index: int, value: int) -> BasisMap:
        self.remove_index(index=index)
        self.number += self.basis ** index * value
        return self
    
    def remove_index(self, index: int) ->  BasisMap:
        value = self.get_value(index=index)
        self.number -= self.basis ** index * value
        return self
    
    def get_value(self, index: int) -> int:
        temp = self.number
        while index > 0:
            index -= 1
            temp = temp // self.basis
        return round(temp % self.basis)
    
    def clear(self) -> BasisMap:
        self.number = 0
        return self

    def associated_number(self) -> int:
        return self.number
    
    def __iter__(self):
        return BasisIter(basis_map=self)

class BasisIter:
    def __init__(self, basis_map: BasisMap) -> None:
        self.basis_map = basis_map
        self.index = -1
    
    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        self.index += 1
        if self.basis_map.basis ** self.index > self.basis_map.associated_number():
            raise StopIteration()
        return (self.index, self.basis_map.get_value(index=self.index))
