# coding: utf-8

import sys
import reader
import systab
import util
import collections
from symbol import Symbol
from data import Data
import opcode
import run

#_text_size = 0
#_data_size = 0
_symbol = 0

def header(bytes):
    # ヘッダーの読み込み    
    global _text_size, _data_size, _symbol

    h = bytes[:16]
    # print("header:", h)

    _text_size = (h[3] << 8) | h[2] # textサイズ
    _data_size = (h[5] << 8) | h[4] # dataサイズ

    print("text size:", _text_size)
    print("data size:", _data_size)

def odump(data):
    def print_format(offset, bytes, dump):
        print("%4x:" % offset, end="") # オフセット
        xs = [] # 16進数で出力
        for i in range(0, len(bytes), 2):
            x = (bytes[i+1] << 8) | bytes[i]
            xs.append(" %04x" % x)
        print("".join(xs).ljust(16), end="")

        d = list(map(str, dump))
        if len(d) == 1:
            s = d[0]
        else:
            s = d[0] + " " + ", ".join(d[1:])
        s = s.ljust(20)
        print(s, end="")

        ys = [] # 8進数で出力
        for i in range(0, len(bytes), 2):
            x = (bytes[i+1] << 8) | bytes[i]
            ys.append(" %06o" % x)
        print("".join(ys))
        pass
    
    offset = 0
    while data.has_more_elements():
        if offset >= _text_size: break
        data.marked()
        op = util.read2(data)

        d = opcode.dispatch(op, data, run.MODE_DUMP, None)
        eatbytes = data.get_readbytes_from_mark() # 読み込んだバイト配列

        # ダンプ
        print_format(offset, eatbytes, d)

        # 読み込んだバイト分、オフセットを進める
        offset += len(data.get_readbytes_from_mark())
    
def dump_symbol(mem):
    symbol_table_size = (mem[9] << 8) | mem[8] # シンボルテーブルのサイズ
    print("symbol table size: %d(0x%x)" % (symbol_table_size, symbol_table_size))

    symbols = []
    p = len(mem) - symbol_table_size
    while p < len(mem):
        name = mem[p:p+8]
        type = (mem[p+9]  << 8) | mem[p+8]
        addr = (mem[p+11] << 8) | mem[p+10]
        p += 12

        t = ""
        for x in name:
            if x == 0: break
            t += chr(x)

        s = Symbol(t, type, addr)
        symbols.append(s)
    return symbols

def dump_my(mem, symbols):
    ss = sorted(symbols, key=lambda a: a.addr)
    for s in ss:
        print(s)

    for i in range(len(ss)):
        sym = ss[i]
        if sym.name.startswith("_"):
            print("name:%s addr:%x" % (sym.name, sym.addr))
            
            next_sym = ss[i+1]
            # print("fm:%x to:%x" % (sym.addr, next_sym.addr))
            fm = sym.addr
            to = next_sym.addr
            print("\t", end="")
            for i in range(fm+16, to+16, 2):
                x = (mem[i+1] << 8) | mem[i]
                print("%04x " % x, end="")
            print("END")

def main():
    filename = sys.argv[1]
    with open(filename, "rb") as fin:
        bytes = fin.read()
        # print("filename:%s size:%d" % (filename, len(data)))

    header(bytes)
    data = Data(bytes[16:])
    odump(data)
    
#    run.run(bytes, run.MODE_DUMP)

#    symbols = dump_symbol(aout)
#    dump_my(aout, symbols)
    
if __name__ == "__main__":
    main()
