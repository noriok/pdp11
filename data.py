# coding: utf-8

class Data:
    def __init__(self, data):
        self.data = data
        self.p = 0
        self.mark = 0

    def read(self, n):
        assert self.p+n <= len(self.data)
        ret = self.data[self.p:self.p+n]
        self.p += n
        return ret

    def set_position(self, p):
        # print("<> set_position:", p)
        self.p = p

    def get_position(self):
        return self.p

    def has_more_elements(self):
        return self.p+1 < len(self.data)

    def marked(self):
        self.mark = self.p

    def get_readbytes_from_mark(self):
        return self.data[self.mark:self.p]

    def ate_bytes(self):
        return self.p
    
if __name__ == "__main__":
    pass
