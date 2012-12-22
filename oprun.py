# coding: utf-8

def _arg(vm, n):
    mode = (n >> 3) & 7
    rn   = (n >> 0) & 7

    val = None # 代入する値
    if mode == 0:   # R     # register
        val = vm.get_reg(rn)

    elif mode == 1: # (R)   # register deferred
        val = vm.get_mem(vm.get_reg(rn))

    elif mode == 2: # (R)+  # auto-increment
        val = vm.get_mem(vm.get_reg(rn))
        vm.inc_reg(rn)

    elif mode == 3: # @(R)+ #  auto-incr deferred
        val = vm.get_mem(vm.get_mem(vm.get_reg(rn)))
        vm.inc_reg(rn)
        
    elif mode == 4: # -(R)  # auto-decrement
        val = vm.get_mem(vm.dec_reg(rn))
        
    elif mode == 5: # @-(R) # auto-decr deferred
        val = vm.get_mem(vm.get_mem(vm.dec_reg(rn)))

    elif mode == 6: # X(R)  # index
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()
        val = vm.get_mem(vm.get_reg(rn) + x)

    elif mode == 7: # @X(R) # index deferred
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()
        val = vm.get_mem(vm.get_mem(vm.get_reg(rn) + x))

    assert val is not None
    return val

def jsr_arg(vm, n):
    mode = (n >> 3) & 7
    rn   = (n >> 0) & 7

    val = None # 代入する値
    if mode == 0:   # R     # register
        val = vm.get_reg(rn)

    elif mode == 1: # (R)   # register deferred
        # val = vm.get_mem(vm.get_reg(rn))
        print("---- jsr_arg rn:%s reg[%d]:%s" % (rn, rn, vm.get_reg(rn)))
        val = vm.get_reg(rn)
        

    elif mode == 2: # (R)+  # auto-increment
        val = vm.get_mem(vm.get_reg(rn))
        vm.inc_reg(rn)

    elif mode == 3: # @(R)+ #  auto-incr deferred
        val = vm.get_mem(vm.get_mem(vm.get_reg(rn)))
        vm.inc_reg(rn)
        
    elif mode == 4: # -(R)  # auto-decrement
        val = vm.get_mem(vm.dec_reg(rn))
        
    elif mode == 5: # @-(R) # auto-decr deferred
        val = vm.get_mem(vm.get_mem(vm.dec_reg(rn)))

    elif mode == 6: # X(R)  # index
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()

        val = vm.get_reg(rn) + x

    elif mode == 7: # @X(R) # index deferred
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()
        val = vm.get_mem(vm.get_mem(vm.get_reg(rn) + x))

    assert val is not None
    return val

def mov(vm, op, data):
    code = op >> 12
    mode1 = (op >> 9) & 7
    rn1   = (op >> 6) & 7
    mode2 = (op >> 3) & 7
    rn2   = (op >> 0) & 7
    
    print("> mov")
    vm.inc_pc() # mov読み飛ばし

    val = None # 代入する値
    if mode1 == 0:   # R     # register
        val = vm.get_reg(rn1)

    elif mode1 == 1: # (R)   # register deferred
        val = vm.get_mem(vm.get_reg(rn1))

    elif mode1 == 2: # (R)+  # auto-increment
        val = vm.get_mem(vm.get_reg(rn1))
        vm.inc_reg(rn1)

    elif mode1 == 3: # @(R)+ #  auto-incr deferred
        val = vm.get_mem(vm.get_mem(vm.get_reg(rn1)))
        vm.inc_reg(rn1)
        
    elif mode1 == 4: # -(R)  # auto-decrement
        val = vm.get_mem(vm.dec_reg(rn1))
        
    elif mode1 == 5: # @-(R) # auto-decr deferred
        val = vm.get_mem(vm.get_mem(vm.dec_reg(rn1)))

    elif mode1 == 6: # X(R)  # index
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()
        val = vm.get_mem(vm.get_reg(rn1) + x)

    elif mode1 == 7: # @X(R) # index deferred
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()
        val = vm.get_mem(vm.get_mem(vm.get_reg(rn1) + x))

    else:
        assert False

    assert val is not None

    
    if mode2 == 0:   # R     # register
        vm.set_reg(rn2, val)

    elif mode2 == 1: # (R)   # register deferred
        memp = vm.get_mem(vm.get_reg(rn2))
        vm.set_mem(memp, val)

    elif mode2 == 2: # (R)+  # auto-increment
        memp = vm.get_mem(vm.get_reg(rn2))
        vm.inc_reg(rn2)

        vm.set_mem(memp, val)

    elif mode2 == 3: # @(R)+ #  auto-incr deferred
        memp = vm.get_mem(vm.get_mem(vm.get_reg(rn2)))
        vm.inc_reg(rn2)

        vm.set_mem(memp, val)
        
    elif mode2 == 4: # -(R)  # auto-decrement
        memp = vm.get_mem(vm.dec_reg(rn2))
        vm.set_mem(memp, val)
        
    elif mode2 == 5: # @-(R) # auto-decr deferred
        memp = vm.get_mem(vm.get_mem(vm.dec_reg(rn2)))
        vm.set_mem(memp, val)

    elif mode2 == 6: # X(R)  # index
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()
        memp = vm.get_mem(vm.get_reg(rn2) + x)
        vm.set_mem(memp, val)

    elif mode2 == 7: # @X(R) # index deferred
        x = vm.get_text_data_2bytes(vm.pc())
        vm.inc_pc()
        memp = vm.get_mem(vm.get_mem(vm.get_reg(rn2) + x))
        vm.set_mem(memp, val)

    else:
        assert False

def rtt(vm, op, data):
    print("> rtt")
    assert False
    pass

def jmp(vm, op, data):
    n = jsr_arg(vm, op & 0b111111)
    print("> jmp n:%s" % (n))
    vm.set_pc(n)

def rts(vm, op, data):
    print("> rts")
    assert False
    pass

def jsr(vm, op, data):
    vm.inc_pc()
    rn = (op >> 6) & 7
    n = jsr_arg(vm, op & 0b111111)
    print("> jsr rn:%s n:%s %s %s" % (rn, n, oct(n), hex(n)))

    if rn != 6:
        vm.set_reg(rn, vm.pc())

    vm.set_pc(n)

def clr(vm, op, data):
    print("> clr")
    assert False
    pass

def tst(vm, op, data):
    print("> tst")
    x = _arg(vm, op & 0b111111)
    vm.set_flag(n=x<0, z=x==0, v=0, c=0)

    vm.inc_pc()

def cmp(vm, op, data):
    print("> cmp")
    assert False
    pass

def bcc(vm, op, data):
    print("> bcc")
    assert False
    pass

def setd(vm, op, data):
    print("> setd")
    vm.inc_pc()
    pass
