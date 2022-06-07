class Decoder:
    @staticmethod
    def decode(code: int, basis: int) -> list:
        res = []
        i = 0
        bc = code
        while basis ** i <= code:
            index = 0
            temp = bc % basis
            bc = bc // basis
            if temp != 0:
                index = temp
            res.append(int(index))
            i += 1
        print(f'decoded shit: {res}')
        return res
