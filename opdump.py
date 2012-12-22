# coding: utf-8

import util

def _r(no):
    if no == 6:
        return "sp"
    if no == 7:
        return "pc"
    return "r%d" % no

def _mov1(mode, rn, data):
    if mode == 0:   # R     # register
        return _r(rn)
    elif mode == 1: # (R)   # register deferred
        return "(%s)" % _r(rn)
    elif mode == 2: # (R)+  # auto-increment
        if rn == 7:
            x = util.read2(data)
            return "$%o" % x
                
        return "(%s)+" % _r(rn)
    elif mode == 3: # @(R)+ # auto-incr deferred
        ret = "@(%s)+" % _r(rn)
        if rn == 7:
            x = util.read2(data)
            return "%s => %d(%s %s)" % (ret, x, oct(x), hex(x))
    elif mode == 4: # -(R)  # auto-decrement
        return "-(%s)" % _r(rn)
    elif mode == 5: # @-(R) # auto-decr deferred
        return "@-(%s)" % _r(rn)
    elif mode == 6: # X(R)  # index
        x = util.read2(data)
        ret = "%s(%s)" % (oct(x), _r(rn))
        if rn == 7:
            return "%s => $%s" % (ret, hex(data.ate_bytes() + x))
        return ret        
    elif mode == 7: # @X(R) # index deferred
        return "@X(%s)" % _r(rn)
    else:
        assert False

    assert False

# 01 SS DD
def mov(op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7

    assert code == 1
    return ["mov", _mov1(mode1, rn1, data), _mov1(mode2, rn2, data)]

# 02 SS DD
def cmp(op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7

    return ["cmp", _mov1(mode1, rn1, data), _mov1(mode2, rn2, data)]

def rtt(op, data):
    return ["rtt"]

# 00 01 DD
def jmp(op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7
    return ["jmp", _mov1(mode2, rn2, data)]

# 00 02 0R
def rts(op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7
    return ["rts", _r(rn2)]
    
# 00 4R DD
def jsr(op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7

    return ["jsr", _r(rn1), _mov1(mode2, rn2, data)]

# 00 50 DD
def clr(op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7
    return ["clr", _mov1(mode2, rn2, data)]
    
# 00 57 DD
def tst(op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7
    
    return ["tst", _mov1(mode2, rn2, data)]

def bcc(op, data):
    # ドキュメントにoffset*2とある
    x = hex(data.ate_bytes() + 2 * (op & 0o77))
    return ["bcc", x]

def setd(op, data):
    return ["setd"]
