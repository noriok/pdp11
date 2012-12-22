# coding: utf-8

import util
import opdump
import oprun
import run

def dispatch(op, data, mode, vm):
    def op_match(a, b):
        assert len(a) == len(b), (len(a), len(b))
        for i in range(len(a)):
            if a[i].isdigit() and b[i].isdigit():
                if a[i] != b[i]:
                    return False
        return True

    if 0o104400 <= op <= 0o104777: # Trap
        # print("TRAP:", op, oct(op))
        return ["sys", (op & 0xff)]

    # TODO: データを読むところを統一する
    if vm is not None:
        data.set_position(vm.pc() + 2) # +2 はop自身の分
    
    op8 = "%06o" % op # 8進に変換
    for (opcode, dumpfn, dofn) in optable:
        opcode = opcode.replace(" ", "")
            
        if op_match(op8, opcode):
            if mode == run.MODE_DUMP:
                return dumpfn(op, data)
            elif mode == run.MODE_EXEC:
                return dofn(vm, op, data)
            else:
                assert False
    else:
        # print("not matched:", op, oct(op), hex(op))
        if mode == run.MODE_DUMP:
            return [".word", oct(op)]
        else:
            assert False, ("unimplement:%d" % opcode)

d = opdump
r = oprun
optable = [
    ("00 00 06", d.rtt, r.rtt),
    ("00 01 DD", d.jmp, r.jmp),
    ("00 02 0R", d.rts, r.rts),
    ("00 4R DD", d.jsr, r.jsr),
    ("00 50 DD", d.clr, r.clr),
    ("00 57 DD", d.tst, r.tst),

    ("01 SS DD", d.mov, r.mov),
    ("02 SS DD", d.cmp, r.cmp),

    ("10 30 XX", d.bcc, r.bcc),

    ("17 00 11", d.setd, r.setd),
]

if __name__ == "__main__":
    pass
