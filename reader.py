# coding: utf-8

class Reader:
    def __init__(self, data):
        self.data = data
        self.p = 0

    def read(self, n):
        ret = self.data[self.p:self.p+n]
        self.p += n
        return ret

    def read_byte(self):
        return self.read(1)

    def has_more_elements(self):
        return self.p+1 < len(self.data)

def test():
    with open("a.out", "rb") as fin:
        data = fin.read()

    r = Reader(data)
    print("a.out:")
    print(r.read_byte())
    print(r.read_byte())
    print(r.read(3))
    print(r.read(2))
    
if __name__ == "__main__":
    r = Reader([3,4,31,5,38,2,0,3])

    test()

    
