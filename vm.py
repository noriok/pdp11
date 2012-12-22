# coding: utf-8

import collections
import util
import sys
import systab

execute = False

class Flags:
    def __init__(self):
        self.n = 0
        self.z = 0
        self.v = 0
        self.c = 0

    def __repr__(self):
        return "[Flags] n:%s z:%s v:%s c:%s" % (self.n, self.z, self.v, self.c)

class VM:
    def __init__(self, text_data):
        self.text_data = text_data
        self.reg = [0] * 8 # register

        self.reg[6] = 0xfff6
        self.mem = [0] * 0xffff # memory
        self.flags = Flags()

    def set_flag(self, n=None, z=None, v=None, c=None):
        # print("[vm] setflag n:%s z:%s v:%s c:%s" % (n, z, v, c))

        if n is not None:
            self.flags.n = n
        if z is not None:
            self.flags.z = z
        if v is not None:
            self.flags.v = v
        if c is not None:
            self.flags.c = c

    def set_reg(self, p, val):
        # print("registerへの格納 reg:%d 値:%d" % (reg, val))
        print("reg[%d] = %d" % (p, val))
        self.reg[p] = val

    def get_reg(self, p):
        # print("registerから取得 reg:%d 格納されている値:%d" % (reg, self.reg[reg]))
        return self.reg[p]
        # return self.reg[reg]

    def inc_reg(self, p): # 2バイトinc
        self.reg[p] += 2
        return self.reg[p]

    def dec_reg(self, p): # 2バイトdec
        self.reg[p] -= 2
        return self.reg[p]

    def inc_pc(self): # プログラムカウンタをインクリメント
        self.inc_reg(7)

    def set_pc(self, n):
        # print("----- set_pc", n)
        self.set_reg(7, n)

    def sp(self):     # スタックポインタ
        return self.reg[6]
    
    def pc(self):     # プログラムカウンタ
        return self.reg[7]

    def dump_reg(self):
        print(",".join(["%04x" % r for r in self.reg]))

    def get_mem(self, p):
        return self.mem[p]
    
    def set_mem(self, p, val):
        print("mem[%d] = %d" % (p, val))
        self.mem[p] = val

    def get_text_data_2bytes(self, p): # 2バイト読み込む
        a = self.text_data[p+1]
        b = self.text_data[p]
        return (a << 8) | b

    def sys(self, index, offset):
        # print("[sys] %s nargs:%d" % (systab.get_name(index), systab.get_nargs(index)))
        
        if index == 1: # exit
            print("sys.exit()を呼び出します reg0の値:%d" % self.reg[0])
            sys.exit(self.reg[0])
            pass
        elif index == 4: # write
            off = offset + 16 # +16はヘッダー分
            off += 2 # 自分自身のオペコード分

            # リトルエンディアンなのでひっくり返す
            address = (self.data[off+1] << 8) | self.data[off] # 文字列データの格納アドレス
            n = (self.data[off+3] << 8) | self.data[off+2]     # 出力文字数
            # print([hex(i) for i in [address, n]])

            for i in range(n):
                c = chr(self.data[16 + address + i]) # 16はヘッダ
                print(c, end="")
        else:
            print("???")

    def run(self):
        pass
            
if __name__ == "__main__":
    main()
