# coding: utf-8

import sys
import util
import opcode
from data import Data
from vm import VM

MODE_DUMP = 0
MODE_EXEC = 1

def run(bytes, mode):
    data = Data(bytes[16:])

    isdump = mode == MODE_DUMP
    offset = 0
    text_bytes = bytes[16:] # テキストデータ
    vm = VM(text_bytes)
    # TODO:dumpとrunは分ける。
    while data.has_more_elements():
        pc = vm.pc()
        op = (text_bytes[pc+1] << 8) | text_bytes[pc]
        print("pc:", pc, hex(pc), "op:", op, oct(op), hex(op))

        # ダンプ用
        d = opcode.dispatch(op, data, MODE_DUMP, vm)
        print("dump:", d)
        # ダンプするとpcが書き換わるので、元に戻す
        vm.set_pc(pc)
        
        d = opcode.dispatch(op, data, mode, vm)


        vm.dump_reg()

def main():
    filename = sys.argv[1]
    with open(filename, "rb") as fin:
        bytes = fin.read()

    run(bytes, MODE_EXEC)
    
if __name__ == "__main__":
    main()
    pass

