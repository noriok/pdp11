# coding: utf-8

def read2(data):
    xs = data.read(2)
    ys = (xs[1] << 8) | xs[0]
    return ys

def read_2(mem, p):
    x = (mem[p+1] << 8) | mem[p]
    return x, p+2
