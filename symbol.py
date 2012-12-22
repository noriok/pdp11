# coding: utf-8

class Symbol:
    def __init__(self, name, type, addr):
        self.name = name
        self.type = type
        self.addr = addr

    def __str__(self):
        return "<name:%s type:0x%x addr:0x%x>" % (self.name, self.type, self.addr)

    def __repr__(self):
        return str(self)

