token_len_map = {
    "Ax":  1,
    "Axl": 1,
    "Axh": 1,
    "Bx": 1,
    "Bxl": 1,
    "Bxh": 1,
    "Bx": 1,
    "Px": 1,
    "R01": 1,
    "R04": 1,
    "R45": 1,
    "Ar": 1,
    "offsZI": 1,
    "stepD2S": 1,
    "stepII2": 1,
    "ArpRn1": 1,
    "ArpStep1": 1,
    "ArRn1": 1,
    "ArStep1": 1,
    "ArStep1Alt": 1,
    "CbsCond": 1,

    "Ab": 2,
    "Abl": 2,
    "Abh": 2,
    "Abe": 2,
    "R0123": 2,
    "R0425": 2,
    "R4567": 2,
    "Arp": 2,
    "offsZIDZ": 2,
    "StepZIDS": 2,
    "modrstepZIDS": 2,
    "stepII2D2S": 2,
    "stepII2D2S0": 2,
    "modrstepII2D2S0": 2,
    "Mul2": 2,
    "ArRn2": 2,
    "ArStep2": 2,
    "ArpRn2": 2,
    "ArpStep2": 2,

    "Ablh": 3,
    "R0123457y0": 3,
    "Rn": 3,
    "ArArp": 3,
    "SttMod": 3,
    "MemRn": 3,
    "Alu": 3,
    "Alb": 3,
    "Mul3": 3,
    "Moda3": 3,
    "RnOld": 3,

    "Cond": 4,
    "ArArpSttMod": 4,
    "SwapType": 4,
    "Alm": 4,
    "Moda4": 4,
    

    "Register": 5,
    "RegisterP0": 5,

    "BankFlags": 6,

}

def get_tok_len(tok: str):
    operand = tok
    if operand.startswith("MemR7"):
        operand = operand[5:]
    elif operand.startswith("Mem"):
        #print(operand[3:])
        operand = operand[3:]
    elif operand.startswith("ProgMem"):
        operand = operand[7:]

    if operand.startswith('Imm'):
        operand = operand[3:]
        operand = operand.strip('s')
        operand = operand.strip('u')
        operand = operand.strip('bitno')
        return int(operand)
    
    if operand.startswith('Unused'):
        operand = operand[6:]
        return int(operand)
    if operand.startswith('Address18'):
        operand = operand[10:]
        return int(operand)
    if operand.startswith('Address16'):
        return 16
    if operand.startswith('RelAddr'):
        operand = operand[7:]
        return int(operand)

    length = token_len_map[operand]
    return length

class Operand:
    op_type = ""
    name = ""
    begin = 0
    end = 0

    def __init__(self, op_type):
        self.op_type = op_type

    def __str__(self):
        return f"{self.op_type}<{self.name}, {begin}, {end}>"

SX = Operand("SX")
SY = Operand("SY")
UY = Operand("UY")
UX = Operand("UX")
BSv = Operand("BSv")
BSr = Operand("BSr")
BZr = Operand("BZr")
Add = Operand("Add")
PP = Operand("PP")
BAc = Operand("BAc")
Sub = Operand("Sub")
PA = Operand("PA")
EMod = Operand("EMod")
DMod = Operand("DMod")

class INST:
    name = ""
    base = 0
    args = []
    def __init__(self, name:str, base: int, *args):
        self.name = name
        self.base = base
        self.args = args

        # print(f"name={name}")

    def EXCEPT(self, *args):
        return self
        pass

def At(operand : str, begin: int):
    op = Operand("At")
    op.name = operand
    op.begin = begin
    op.end = op.begin + get_tok_len(operand) - 1
    return op

def Const(operand : str, begin: int):
    op = Operand("Const")
    op.name = operand
    op.begin = begin
    return op

def Unused(begin: int):
    op = Operand("Unused")
    op.name = "Unused"
    op.begin = begin
    op.end = begin
    return op

def AtConst(operand : str, begin: int, end: int):
    op = Operand("AtConst")
    op.name = operand
    op.begin = begin
    return op
    
def AtNamed(operand : str, begin: int):
    return At(operand, begin)


instr = [
    # <<< Misc >>>
    INST("nop", 0x0000),
    INST("norm", 0x94C0, At("Ax", 8), At("Rn", 0), At("StepZIDS", 3)),
    INST("swap", 0x4980, At("SwapType", 0)),
    INST("trap", 0x0020),

    # <<< ALM normal >>>
    INST("alm", 0xA000, At("Alm", 9), At("MemImm8", 0), At("Ax", 8)),
    INST("alm", 0x8080, At("Alm", 9), At("Rn", 0), At("StepZIDS", 3), At("Ax", 8)),
    INST("alm", 0x80A0, At("Alm", 9), At("Register", 0), At("Ax", 8)),

    # <<< ALM r6 >>>
    INST("alm_r6", 0xD388, Const("Alm", 0), At("Ax", 4)),
    INST("alm_r6", 0xD389, Const("Alm", 1), At("Ax", 4)),
    INST("alm_r6", 0xD38A, Const("Alm", 2), At("Ax", 4)),
    INST("alm_r6", 0xD38B, Const("Alm", 3), At("Ax", 4)),
    INST("alm_r6", 0xD38C, Const("Alm", 4), At("Ax", 4)),
    INST("alm_r6", 0xD38D, Const("Alm", 5), At("Ax", 4)),
    INST("alm_r6", 0xD38E, Const("Alm", 6), At("Ax", 4)),
    INST("alm_r6", 0xD38F, Const("Alm", 7), At("Ax", 4)),
    INST("alm_r6", 0x9462, Const("Alm", 8), At("Ax", 0)),
    INST("alm_r6", 0x9464, Const("Alm", 9), At("Ax", 0)),
    INST("alm_r6", 0x9466, Const("Alm", 10), At("Ax", 0)),
    INST("alm_r6", 0x5E23, Const("Alm", 11), At("Ax", 8)),
    INST("alm_r6", 0x5E22, Const("Alm", 12), At("Ax", 8)),
    INST("alm_r6", 0x5F41, Const("Alm", 13), Const("Ax", 0)),
    INST("alm_r6", 0x9062, Const("Alm", 14), At("Ax", 8), Unused(0)),
    INST("alm_r6", 0x8A63, Const("Alm", 15), At("Ax", 3)),

    # <<< ALU normal >>>
    INST("alu", 0xD4F8, At("Alu", 0), At("MemImm16", 16), At("Ax", 8))
        .EXCEPT(AtConst("Alu", 0, 4)).EXCEPT(AtConst("Alu", 0, 5)),
    INST("alu", 0xD4D8, At("Alu", 0), At("MemR7Imm16", 16), At("Ax", 8))
        .EXCEPT(AtConst("Alu", 0, 4)).EXCEPT(AtConst("Alu", 0, 5)),
    INST("alu", 0x80C0, At("Alu", 9), At("Imm16", 16), At("Ax", 8))
        .EXCEPT(AtConst("Alu", 9, 4)).EXCEPT(AtConst("Alu", 9, 5)),
    INST("alu", 0xC000, At("Alu", 9), At("Imm8", 0), At("Ax", 8))
        .EXCEPT(AtConst("Alu", 9, 4)).EXCEPT(AtConst("Alu", 9, 5)),
    INST("alu", 0x4000, At("Alu", 9), At("MemR7Imm7s", 0), At("Ax", 8))
        .EXCEPT(AtConst("Alu", 9, 4)).EXCEPT(AtConst("Alu", 9, 5)),

    # <<< OR Extra >>>
    INST("or_", 0xD291, At("Ab", 10), At("Ax", 6), At("Ax", 5)),
    INST("or_", 0xD4A4, At("Ax", 8), At("Bx", 1), At("Ax", 0)),
    INST("or_", 0xD3C4, At("Bx", 10), At("Bx", 1), At("Ax", 0)),

    # <<< ALB normal >>>
    INST("alb", 0xE100, At("Alb", 9), At("Imm16", 16), At("MemImm8", 0)),
    INST("alb", 0x80E0, At("Alb", 9), At("Imm16", 16), At("Rn", 0), At("StepZIDS", 3)),
    INST("alb", 0x81E0, At("Alb", 9), At("Imm16", 16), At("Register", 0)),
    INST("alb_r6", 0x47B8, At("Alb", 0), At("Imm16", 16)),

    # <<< ALB SttMod >>>
    INST("alb", 0x43C8, Const("Alb", 0), At("Imm16", 16), At("SttMod", 0)),
    INST("alb", 0x4388, Const("Alb", 1), At("Imm16", 16), At("SttMod", 0)),
    INST("alb", 0x0038, Const("Alb", 2), At("Imm16", 16), At("SttMod", 0)),
    #INST(alb, 0x????, Const<Alb, 3>, At<Imm,16, 16>, At<SttMod, 0>),
    INST("alb", 0x9470, Const("Alb", 4), At("Imm16", 16), At("SttMod", 0)),
    INST("alb", 0x9478, Const("Alb", 5), At("Imm16", 16), At("SttMod", 0)),
    #INST(alb, 0x????, Const<Alb, 6>, At<Imm,16, 16>, At<SttMod, 0>),
    #INST(alb, 0x????, Const<Alb, 7>, At<Imm,16, 16>, At<SttMod, 0>),

    # <<< Add extra >>>
    INST("add", 0xD2DA, At("Ab", 10), At("Bx", 0)),
    INST("add", 0x5DF0, At("Bx", 1), At("Ax", 0)),
    INST("add_p1", 0xD782, At("Ax", 0)),
    INST("add", 0x5DF8, At("Px", 1), At("Bx", 0)),

    # <<< Sub extra >>>
    INST("sub", 0x8A61, At("Ab", 3), At("Bx", 8)),
    INST("sub", 0x8861, At("Bx", 4), At("Ax", 3)),
    INST("sub_p1", 0xD4B9, At("Ax", 8)),
    INST("sub", 0x8FD0, At("Px", 1), At("Bx", 0)),

    ## <<< addsub p0 p1 >>>
    INST("app", 0x5DC0, At("Ab", 2), BZr, Add, PP, Add, PP),
    INST("app", 0x5DC1, At("Ab", 2), BZr, Add, PP, Add, PA),
    INST("app", 0x4590, At("Ab", 2), BAc, Add, PP, Add, PP),
    INST("app", 0x4592, At("Ab", 2), BAc, Add, PP, Add, PA),
    INST("app", 0x4593, At("Ab", 2), BAc, Add, PA, Add, PA),
    INST("app", 0x5DC2, At("Ab", 2), BZr, Add, PP, Sub, PP),
    INST("app", 0x5DC3, At("Ab", 2), BZr, Add, PP, Sub, PA),
    INST("app", 0x80C6, At("Ab", 10), BAc, Sub, PP, Sub, PP),
    INST("app", 0x82C6, At("Ab", 10), BAc, Sub, PP, Sub, PA),
    INST("app", 0x83C6, At("Ab", 10), BAc, Sub, PA, Sub, PA),
    INST("app", 0x906C, At("Ab", 0), BAc, Add, PP, Sub, PP),
    INST("app", 0x49C2, At("Ab", 4), BAc, Sub, PP, Add, PP),
    INST("app", 0x916C, At("Ab", 0), BAc, Add, PP, Sub, PA),
    INST("app", 0x49C3, At("Ab", 4), BAc, Sub, PP, Add, PA),

    ## <<< add||sub >>>
    INST("add_add", 0x6F80, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 3)),
    INST("add_sub", 0x6FA0, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 3)),
    INST("sub_add", 0x6FC0, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 3)),
    INST("sub_sub", 0x6FE0, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 3)),

    ## <<< add||sub sv >>>
    INST("add_sub_sv", 0x5DB0, At("ArRn1", 1), At("ArStep1", 0), At("Ab", 2)),
    INST("sub_add_sv", 0x5DE0, At("ArRn1", 1), At("ArStep1", 0), At("Ab", 2)),

    ## <<< add||sub||mov sv >>>
    INST("sub_add_i_mov_j_sv", 0x8064, At("ArpRn1", 8), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 3)),
    INST("sub_add_j_mov_i_sv", 0x5D80, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 3)),
    INST("add_sub_i_mov_j", 0x9070, At("ArpRn1", 8), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 2)),
    INST("add_sub_j_mov_i", 0x5E30, At("ArpRn1", 8), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 2)),

    # <<< Mul >>>
    INST("mul", 0x8000, At("Mul3", 8), At("Rn", 0), At("StepZIDS", 3), At("Imm16", 16), At("Ax", 11)),
    INST("mul_y0", 0x8020, At("Mul3", 8), At("Rn", 0), At("StepZIDS", 3), At("Ax", 11)),
    INST("mul_y0", 0x8040, At("Mul3", 8), At("Register", 0), At("Ax", 11)),
    INST("mul", 0xD000, At("Mul3", 8), At("R45", 2), At("StepZIDS", 5), At("R0123", 0), At("StepZIDS", 3), At("Ax", 11)),
    INST("mul_y0_r6", 0x5EA0, At("Mul3", 1), At("Ax", 0)),
    INST("mul_y0", 0xE000, At("Mul2", 9), At("MemImm8", 0), At("Ax", 11)),

    # <<< Mul Extra >>>
    INST("mpyi", 0x0800, At("Imm8s", 0)),
    INST("msu", 0xD080, At("R45", 2), At("StepZIDS", 5), At("R0123", 0), At("StepZIDS", 3), At("Ax", 8)),
    INST("msu", 0x90C0, At("Rn", 0), At("StepZIDS", 3), At("Imm16", 16), At("Ax", 8)),
    INST("msusu", 0x8264, At("ArRn2", 3), At("ArStep2", 0), At("Ax", 8)),
    INST("mac_x1to0", 0x4D84, At("Ax", 1), Unused(0)),
    INST("mac1", 0x5E28, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), At("Ax", 8)),

    # <<< MODA >>>
    INST("moda4", 0x6700, At("Moda4", 4), At("Ax", 12), At("Cond", 0))
        .EXCEPT(AtConst("Moda4", 4, 7)),
    INST("moda3", 0x6F00, At("Moda3", 4), At("Bx", 12), At("Cond", 0)),
    INST("pacr1", 0xD7C2, At("Ax", 0)),
    INST("clr", 0x8ED0, At("Ab", 2), At("Ab", 0)),
    INST("clrr", 0x8DD0, At("Ab", 2), At("Ab", 0)),

    # <<< Block repeat >>>
    INST("bkrep", 0x5C00, At("Imm8", 0), At("Address16", 16)),
    INST("bkrep", 0x5D00, At("Register", 0), At("Address18_16", 16), At("Address18_2", 5)),
    INST("bkrep_r6", 0x8FDC, At("Address18_16", 16), At("Address18_2", 0)),
    INST("bkreprst", 0xDA9C, At("ArRn2", 0)),
    INST("bkreprst_memsp", 0x5F48, Unused(0), Unused(1)),
    INST("bkrepsto", 0xDADC, At("ArRn2", 0), Unused(10)),
    INST("bkrepsto_memsp", 0x9468, Unused(0), Unused(1), Unused(2)),

    # <<< Bank >>>
    INST("banke", 0x4B80, At("BankFlags", 0)),
    INST("bankr", 0x8CDF),
    INST("bankr", 0x8CDC, At("Ar", 0)),
    INST("bankr", 0x8CD0, At("Ar", 2), At("Arp", 0)),
    INST("bankr", 0x8CD8, At("Arp", 0)),

    # <<< Bitrev >>>
    INST("bitrev", 0x5EB8, At("Rn", 0)),
    INST("bitrev_dbrv", 0xD7E8, At("Rn", 0)),
    INST("bitrev_ebrv", 0xD7E0, At("Rn", 0)),

    # <<< Branching >>>
    INST("br", 0x4180, At("Address18_16", 16), At("Address18_2", 4), At("Cond", 0)),
    INST("brr", 0x5000, At("RelAddr7", 4), At("Cond", 0)),

    # <<< Break >>>
    INST("break_", 0xD3C0),

    # <<< Call >>>
    INST("call", 0x41C0, At("Address18_16", 16), At("Address18_2", 4), At("Cond", 0)),
    INST("calla", 0xD480, At("Axl", 8)),
    INST("calla", 0xD381, At("Ax", 4)),
    INST("callr", 0x1000, At("RelAddr7", 4), At("Cond", 0)),

    # <<< Context >>>
    INST("cntx_s", 0xD380),
    INST("cntx_r", 0xD390),

    # <<< Return >>>
    INST("ret", 0x4580, At("Cond", 0)),
    INST("retd", 0xD780),
    INST("reti", 0x45C0, At("Cond", 0)),
    INST("retic", 0x45D0, At("Cond", 0)),
    INST("retid", 0xD7C0),
    INST("retidc", 0xD3C3),
    INST("rets", 0x0900, At("Imm8", 0)),

    # <<< Load >>>
    INST("load_ps", 0x4D80, At("Imm2", 0)),
    INST("load_stepi", 0xDB80, At("Imm7s", 0)),
    INST("load_stepj", 0xDF80, At("Imm7s", 0)),
    INST("load_page", 0x0400, At("Imm8", 0)),
    INST("load_modi", 0x0200, At("Imm9", 0)),
    INST("load_modj", 0x0A00, At("Imm9", 0)),
    INST("load_movpd", 0xD7D8, At("Imm2", 1), Unused(0)),
    INST("load_ps01", 0x0010, At("Imm4", 0)),

    # <<< Push >>>
    INST("push", 0x5F40, At("Imm16", 16)),
    INST("push", 0x5E40, At("Register", 0)),
    INST("push", 0xD7C8, At("Abe", 1), Unused(0)),
    INST("push", 0xD3D0, At("ArArpSttMod", 0)),
    INST("push_prpage", 0xD7FC, Unused(0), Unused(1)),
    INST("push", 0xD78C, At("Px", 1), Unused(0)),
    INST("push_r6", 0xD4D7, Unused(5)),
    INST("push_repc", 0xD7F8, Unused(0), Unused(1)),
    INST("push_x0", 0xD4D4, Unused(5)),
    INST("push_x1", 0xD4D5, Unused(5)),
    INST("push_y1", 0xD4D6, Unused(5)),
    INST("pusha", 0x4384, At("Ax", 6), Unused(0), Unused(1)),
    INST("pusha", 0xD788, At("Bx", 1), Unused(0)),

    # <<< Pop >>>
    INST("pop", 0x5E60, At("Register", 0)),
    INST("pop", 0x47B4, At("Abe", 0)),
    INST("pop", 0x80C7, At("ArArpSttMod", 8)),
    INST("pop", 0x0006, At("Bx", 5), Unused(0)),
    INST("pop_prpage", 0xD7F4, Unused(0), Unused(1)),
    INST("pop", 0xD496, At("Px", 0)),
    INST("pop_r6", 0x0024, Unused(0)),
    INST("pop_repc", 0xD7F0, Unused(0), Unused(1)),
    INST("pop_x0", 0xD494),
    INST("pop_x1", 0xD495),
    INST("pop_y1", 0x0004, Unused(0)),
    INST("popa", 0x47B0, At("Ab", 0)),

    # <<< Repeat >>>
    INST("rep", 0x0C00, At("Imm8", 0)),
    INST("rep", 0x0D00, At("Register", 0)),
    INST("rep_r6", 0x0002, Unused(0)),

    # <<< Shift >>>
    INST("shfc", 0xD280, At("Ab", 10), At("Ab", 5), At("Cond", 0)),
    INST("shfi", 0x9240, At("Ab", 10), At("Ab", 7), At("Imm6s", 0)),

    # <<< TSTB >>>
    INST("tst4b", 0x80C1, At("ArRn2", 10), At("ArStep2", 8)),
    INST("tst4b", 0x4780, At("ArRn2", 2), At("ArStep2", 0), At("Ax", 4)),
    INST("tstb", 0xF000, At("MemImm8", 0), At("Imm4", 8)),
    INST("tstb", 0x9020, At("Rn", 0), At("StepZIDS", 3), At("Imm4", 8)),
    INST("tstb", 0x9000, At("Register", 0), At("Imm4", 8))
        .EXCEPT(AtConst("Register", 0, 24)), # override by tstb_r6
    INST("tstb_r6", 0x9018, At("Imm4", 8)),
    INST("tstb", 0x0028, At("SttMod", 0), At("Imm16", 16)), # unused12@20

    # <<< AND Extra >>>
    INST("and_", 0x6770, At("Ab", 2), At("Ab", 0), At("Ax", 12)),

    # <<< Interrupt >>>
    INST("dint", 0x43C0),
    INST("eint", 0x4380),

    # <<< EXP >>>
    INST("exp", 0x9460, At("Bx", 0)),
    INST("exp", 0x9060, At("Bx", 0), At("Ax", 8)),
    INST("exp", 0x9C40, At("Rn", 0), At("StepZIDS", 3)),
    INST("exp", 0x9840, At("Rn", 0), At("StepZIDS", 3), At("Ax", 8)),
    INST("exp", 0x9440, At("Register", 0)),
    INST("exp", 0x9040, At("Register", 0), At("Ax", 8)),
    INST("exp_r6", 0xD7C1),
    INST("exp_r6", 0xD382, At("Ax", 4)),

    # <<< MODR >>>
    INST("modr", 0x0080, At("Rn", 0), At("StepZIDS", 3)),
    INST("modr_dmod", 0x00A0, At("Rn", 0), At("StepZIDS", 3)),
    INST("modr_i2", 0x4990, At("Rn", 0)),
    INST("modr_i2_dmod", 0x4998, At("Rn", 0)),
    INST("modr_d2", 0x5DA0, At("Rn", 0)),
    INST("modr_d2_dmod", 0x5DA8, At("Rn", 0)),
    INST("modr_eemod", 0xD294, At("ArpRn2", 10), At("ArpStep2", 0), At("ArpStep2", 5)),
    INST("modr_edmod", 0x0D80, At("ArpRn2", 5), At("ArpStep2", 1), At("ArpStep2", 3)),
    INST("modr_demod", 0x8464, At("ArpRn2", 8), At("ArpStep2", 0), At("ArpStep2", 3)),
    INST("modr_ddmod", 0x0D81, At("ArpRn2", 5), At("ArpStep2", 1), At("ArpStep2", 3)),

    # <<< MOV >>>
    INST("mov", 0xD290, At("Ab", 10), At("Ab", 5)),
    INST("mov_dvm", 0xD298, At("Abl", 10)),
    INST("mov_x0", 0xD2D8, At("Abl", 10)),
    INST("mov_x1", 0xD394, At("Abl", 0)),
    INST("mov_y1", 0xD384, At("Abl", 0)),

    INST("mov", 0x3000, At("Ablh", 9), At("MemImm8", 0)),
    INST("mov", 0xD4BC, At("Axl", 8), At("MemImm16", 16)),
    INST("mov", 0xD49C, At("Axl", 8), At("MemR7Imm16", 16)),
    INST("mov", 0xDC80, At("Axl", 8), At("MemR7Imm7s", 0)),

    INST("mov", 0xD4B8, At("MemImm16", 16), At("Ax", 8)),
    INST("mov", 0x6100, At("MemImm8", 0), At("Ab", 11)),
    INST("mov", 0x6200, At("MemImm8", 0), At("Ablh", 10)),
    INST("mov_eu", 0x6500, At("MemImm8", 0), At("Axh", 12)),
    INST("mov", 0x6000, At("MemImm8", 0), At("RnOld", 10)),
    INST("mov_sv", 0x6D00, At("MemImm8", 0)),

    INST("mov_dvm_to", 0xD491, At("Ab", 5)),
    INST("mov_icr_to", 0xD492, At("Ab", 5)),

    INST("mov", 0x5E20, At("Imm16", 16), At("Bx", 8)),
    INST("mov", 0x5E00, At("Imm16", 16), At("Register", 0)),
    INST("mov_icr", 0x4F80, At("Imm5", 0)),
    INST("mov", 0x2500, At("Imm8s", 0), At("Axh", 12)),
    INST("mov_ext0", 0x2900, At("Imm8s", 0)),
    INST("mov_ext1", 0x2D00, At("Imm8s", 0)),
    INST("mov_ext2", 0x3900, At("Imm8s", 0)),
    INST("mov_ext3", 0x3D00, At("Imm8s", 0)),
    INST("mov", 0x2300, At("Imm8s", 0), At("RnOld", 10)),
    INST("mov_sv", 0x0500, At("Imm8s", 0)),
    INST("mov", 0x2100, At("Imm8", 0), At("Axl", 12)),

    INST("mov", 0xD498, At("MemR7Imm16", 16), At("Ax", 8)),
    INST("mov", 0xD880, At("MemR7Imm7s", 0), At("Ax", 8)),
    INST("mov", 0x98C0, At("Rn", 0), At("StepZIDS", 3), At("Bx", 8)),
    INST("mov", 0x1C00, At("Rn", 0), At("StepZIDS", 3), At("Register", 5)),

    INST("mov_memsp_to", 0x47E0, At("Register", 0)),
    INST("mov_mixp_to", 0x47C0, At("Register", 0)),
    INST("mov", 0x2000, At("RnOld", 9), At("MemImm8", 0)),
    INST("mov_icr", 0x4FC0, At("Register", 0)),
    INST("mov_mixp", 0x5E80, At("Register", 0)),
    INST("mov", 0x1800, At("Register", 5), At("Rn", 0), At("StepZIDS", 3))
        .EXCEPT(AtConst("Register", 5, 24)).EXCEPT(AtConst("Register", 5, 25)), # override by mov_r6(_to)
    INST("mov", 0x5EC0, At("Register", 0), At("Bx", 5)),
    INST("mov", 0x5800, At("Register", 0), At("Register", 5))
        .EXCEPT(AtConst("Register", 0, 24)).EXCEPT(AtConst("Register", 0, 25)), # override by mma_mov
    INST("mov_repc_to", 0xD490, At("Ab", 5)),
    INST("mov_sv_to", 0x7D00, At("MemImm8", 0)),
    INST("mov_x0_to", 0xD493, At("Ab", 5)),
    INST("mov_x1_to", 0x49C1, At("Ab", 4)),
    INST("mov_y1_to", 0xD299, At("Ab", 10)),

    # <<< MOV load >>>
    INST("mov", 0x0008, At("Imm16", 16), At("ArArp", 0)),
    INST("mov_r6", 0x0023, At("Imm16", 16)),
    INST("mov_repc", 0x0001, At("Imm16", 16)),
    INST("mov_stepi0", 0x8971, At("Imm16", 16)),
    INST("mov_stepj0", 0x8979, At("Imm16", 16)),
    INST("mov", 0x0030, At("Imm16", 16), At("SttMod", 0)),
    INST("mov_prpage", 0x5DD0, At("Imm4", 0)),

    # <<< <<< MOV p/d >>>
    INST("movd", 0x5F80, At("R0123", 0), At("StepZIDS", 3), At("R45", 2), At("StepZIDS", 5)),
    INST("movp", 0x0040, At("Axl", 5), At("Register", 0)),
    INST("movp", 0x0D40, At("Ax", 5), At("Register", 0)),
    INST("movp", 0x0600, At("Rn", 0), At("StepZIDS", 3), At("R0123", 5), At("StepZIDS", 7)),
    INST("movpdw", 0xD499, At("Ax", 8)),

    # <<< MOV 2 >>>
    INST("mov_a0h_stepi0", 0xD49B),
    INST("mov_a0h_stepj0", 0xD59B),
    INST("mov_stepi0_a0h", 0xD482),
    INST("mov_stepj0_a0h", 0xD582),

    INST("mov_prpage", 0x9164, At("Abl", 0)),
    INST("mov_repc", 0x9064, At("Abl", 0)),
    INST("mov", 0x9540, At("Abl", 3), At("ArArp", 0)),
    INST("mov", 0x9C60, At("Abl", 3), At("SttMod", 0)),

    INST("mov_prpage_to", 0x5EB0, At("Abl", 0)),
    INST("mov_repc_to", 0xD2D9, At("Abl", 10)),
    INST("mov", 0x9560, At("ArArp", 0), At("Abl", 3)),
    INST("mov", 0xD2F8, At("SttMod", 0), At("Abl", 10)),

    INST("mov_repc_to", 0xD7D0, At("ArRn1", 1), At("ArStep1", 0)),
    INST("mov", 0xD488, At("ArArp", 0), At("ArRn1", 8), At("ArStep1", 5)),
    INST("mov", 0x49A0, At("SttMod", 0), At("ArRn1", 4), At("ArStep1", 3)),

    INST("mov_repc", 0xD7D4, At("ArRn1", 1), At("ArStep1", 0)),
    INST("mov", 0x8062, At("ArRn1", 4), At("ArStep1", 3), At("ArArp", 8)),
    INST("mov", 0x8063, At("ArRn1", 4), At("ArStep1", 3), At("SttMod", 8)),

    INST("mov_repc_to", 0xD3C8, At("MemR7Imm16", 16), Unused(0), Unused(1), Unused(2)),
    INST("mov", 0x5F50, At("ArArpSttMod", 0), At("MemR7Imm16", 16)),

    INST("mov_repc", 0xD2DC, At("MemR7Imm16", 16), Unused(0), Unused(1), Unused(10)),
    INST("mov", 0x4D90, At("MemR7Imm16", 16), At("ArArpSttMod", 0)),

    INST("mov_pc", 0x886B, At("Ax", 8)),
    INST("mov_pc", 0x8863, At("Bx", 8)),

    INST("mov_mixp_to", 0x8A73, At("Bx", 3)),
    INST("mov_mixp_r6", 0x4381),
    INST("mov_p0h_to", 0x4382, At("Bx", 0)),
    INST("mov_p0h_r6", 0xD3C2),
    INST("mov_p0h_to", 0x4B60, At("Register", 0)),
    INST("mov_p0", 0x8FD4, At("Ab", 0)),
    INST("mov_p1_to", 0x8FD8, At("Ab", 0)),

    INST("mov2", 0x88D0, At("Px", 1), At("ArRn2", 8), At("ArStep2", 2)),
    INST("mov2s", 0x88D1, At("Px", 1), At("ArRn2", 8), At("ArStep2", 2)),
    INST("mov2", 0xD292, At("ArRn2", 10), At("ArStep2", 5), At("Px", 0)),
    INST("mova", 0x4DC0, At("Ab", 4), At("ArRn2", 2), At("ArStep2", 0)),
    INST("mova", 0x4BC0, At("ArRn2", 2), At("ArStep2", 0), At("Ab", 4)),

    INST("mov_r6_to", 0xD481, At("Bx", 8)),
    INST("mov_r6_mixp", 0x43C1),
    INST("mov_r6_to", 0x5F00, At("Register", 0)),
    INST("mov_r6", 0x5F60, At("Register", 0)),
    INST("mov_memsp_r6", 0xD29C, Unused(0), Unused(1), Unused(10)),
    INST("mov_r6_to", 0x1B00, At("Rn", 0), At("StepZIDS", 3)),
    INST("mov_r6", 0x1B20, At("Rn", 0), At("StepZIDS", 3)),

    INST("movs", 0x6300, At("MemImm8", 0), At("Ab", 11)),
    INST("movs", 0x0180, At("Rn", 0), At("StepZIDS", 3), At("Ab", 5)),
    INST("movs", 0x0100, At("Register", 0), At("Ab", 5)),
    INST("movs_r6_to", 0x5F42, At("Ax", 0)),
    INST("movsi", 0x4080, At("RnOld", 9), At("Ab", 5), At("Imm5s", 0)),

    # <<< MOV MOV >>>
    INST("mov2_axh_m_y0_m", 0x4390, At("Axh", 6), At("ArRn2", 2), At("ArStep2", 0)),
    INST("mov2_ax_mij", 0x43A0, At("Ab", 3), At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1)),
    INST("mov2_ax_mji", 0x43E0, At("Ab", 3), At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1)),
    INST("mov2_mij_ax", 0x80C4, At("ArpRn1", 9), At("ArpStep1", 0), At("ArpStep1", 8), At("Ab", 10)),
    INST("mov2_mji_ax", 0xD4C0, At("ArpRn1", 5), At("ArpStep1", 0), At("ArpStep1", 1), At("Ab", 2)),
    INST("mov2_abh_m", 0x9D40, At("Abh", 4), At("Abh", 2), At("ArRn1", 1), At("ArStep1", 0)),
    INST("exchange_iaj", 0x8C60, At("Axh", 4), At("ArpRn2", 8), At("ArpStep2", 0), At("ArpStep2", 2)),
    INST("exchange_riaj", 0x7F80, At("Axh", 6), At("ArpRn2", 4), At("ArpStep2", 0), At("ArpStep2", 2)),
    INST("exchange_jai", 0x4900, At("Axh", 6), At("ArpRn2", 4), At("ArpStep2", 0), At("ArpStep2", 2)),
    INST("exchange_rjai", 0x4800, At("Axh", 6), At("ArpRn2", 4), At("ArpStep2", 0), At("ArpStep2", 2)),

    # <<< MOVR >>>
    INST("movr", 0x8864, At("ArRn2", 3), At("ArStep2", 0), At("Abh", 8)),
    INST("movr", 0x9CE0, At("Rn", 0), At("StepZIDS", 3), At("Ax", 8)),
    INST("movr", 0x9CC0, At("Register", 0), At("Ax", 8)),
    INST("movr", 0x5DF4, At("Bx", 1), At("Ax", 0)),
    INST("movr_r6_to", 0x8961, At("Ax", 3)),

    # <<< LIM >>>
    INST("lim", 0x49C0, At("Ax", 5), At("Ax", 4)),

    # <<< Viterbi >>>
    INST("vtrclr0", 0x5F45),
    INST("vtrclr1", 0x5F46),
    INST("vtrclr", 0x5F47),
    INST("vtrmov0", 0xD29A, At("Axl", 0)),
    INST("vtrmov1", 0xD69A, At("Axl", 0)),
    INST("vtrmov", 0xD383, At("Axl", 4)),
    INST("vtrshr", 0xD781),

    # <<< CLRP >>>
    INST("clrp0", 0x5DFE),
    INST("clrp1", 0x5DFD),
    INST("clrp", 0x5DFF),

    # <<< min/max >>>
    INST("max_ge", 0x8460, At("Ax", 8), At("StepZIDS", 3)),
    INST("max_gt", 0x8660, At("Ax", 8), At("StepZIDS", 3)),
    INST("min_le", 0x8860, At("Ax", 8), At("StepZIDS", 3)),
    INST("min_lt", 0x8A60, At("Ax", 8), At("StepZIDS", 3)),
    INST("max_ge_r0", 0x8060, At("Ax", 8), At("StepZIDS", 3)),
    INST("max_gt_r0", 0x8260, At("Ax", 8), At("StepZIDS", 3)),
    INST("min_le_r0", 0x47A0, At("Ax", 3), At("StepZIDS", 0)),
    INST("min_lt_r0", 0x47A4, At("Ax", 3), At("StepZIDS", 0)),

    # <<< Division Step >>>
    INST("divs", 0x0E00, At("MemImm8", 0), At("Ax", 8)),

    # <<< Sqr >>>
    INST("sqr_sqr_add3", 0xD790, At("Ab", 2), At("Ab", 0)),
    INST("sqr_sqr_add3", 0x4B00, At("ArRn2", 4), At("ArStep2", 2), At("Ab", 0)),
    INST("sqr_mpysu_add3a", 0x49C4, At("Ab", 4), At("Ab", 0)),

    # <<< CMP Extra >>>
    INST("cmp", 0x4D8C, At("Ax", 1), At("Bx", 0)),
    INST("cmp_b0_b1", 0xD483),
    INST("cmp_b1_b0", 0xD583),
    INST("cmp", 0xDA9A, At("Bx", 10), At("Ax", 0)),
    INST("cmp_p1_to", 0x8B63, At("Ax", 4)),

    # <<< min||max||vtrshr >>>
    INST("max2_vtr", 0x5E21, At("Ax", 8)),
    INST("min2_vtr", 0x43C2, At("Ax", 0)),
    INST("max2_vtr", 0xD784, At("Ax", 1), At("Bx", 0)),
    INST("min2_vtr", 0xD4BA, At("Ax", 8), At("Bx", 0)),
    INST("max2_vtr_movl", 0x4A40, At("Ax", 3), At("Bx", 4), At("ArRn1", 1), At("ArStep1", 0)),
    INST("max2_vtr_movh", 0x4A44, At("Ax", 3), At("Bx", 4), At("ArRn1", 1), At("ArStep1", 0)),
    INST("max2_vtr_movl", 0x4A60, At("Bx", 4), At("Ax", 3), At("ArRn1", 1), At("ArStep1", 0)),
    INST("max2_vtr_movh", 0x4A64, At("Bx", 4), At("Ax", 3), At("ArRn1", 1), At("ArStep1", 0)),
    INST("min2_vtr_movl", 0x4A00, At("Ax", 3), At("Bx", 4), At("ArRn1", 1), At("ArStep1", 0)),
    INST("min2_vtr_movh", 0x4A04, At("Ax", 3), At("Bx", 4), At("ArRn1", 1), At("ArStep1", 0)),
    INST("min2_vtr_movl", 0x4A20, At("Bx", 4), At("Ax", 3), At("ArRn1", 1), At("ArStep1", 0)),
    INST("min2_vtr_movh", 0x4A24, At("Bx", 4), At("Ax", 3), At("ArRn1", 1), At("ArStep1", 0)),
    INST("max2_vtr_movij", 0xD590, At("Ax", 6), At("Bx", 5), At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1)),
    INST("max2_vtr_movji", 0x45A0, At("Ax", 4), At("Bx", 3), At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1)),
    INST("min2_vtr_movij", 0xD2B8, At("Ax", 11), At("Bx", 10), At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1)),
    INST("min2_vtr_movji", 0x45E0, At("Ax", 4), At("Bx", 3), At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1)),

    # <<< MOV ADDSUB >>>
    INST("mov_sv_app", 0x4B40, At("ArRn1", 3), At("ArStep1", 2), At("Bx", 0), BSv, Sub, PP, Add, PP),
    INST("mov_sv_app", 0x9960, At("ArRn1", 4), At("ArStep1Alt", 3), At("Bx", 2), BSv, Sub, PP, Add, PP),
    INST("mov_sv_app", 0x4B42, At("ArRn1", 3), At("ArStep1", 2), At("Bx", 0), BSr, Sub, PP, Add, PP),
    INST("mov_sv_app", 0x99E0, At("ArRn1", 4), At("ArStep1Alt", 3), At("Bx", 2), BSr, Sub, PP, Add, PP),
    INST("mov_sv_app", 0x5F4C, At("ArRn1", 1), At("ArStep1", 0), Const("Bx", 0), BSv, Sub, PP, Sub, PP),
    INST("mov_sv_app", 0x8873, At("ArRn1", 8), At("ArStep1", 3), Const("Bx", 1), BSv, Sub, PP, Sub, PP),
    INST("mov_sv_app", 0x9860, At("ArRn1", 4), At("ArStep1Alt", 3), At("Bx", 2), BSv, Sub, PP, Sub, PP),
    INST("mov_sv_app", 0xDE9C, At("ArRn1", 1), At("ArStep1", 0), Const("Bx", 0), BSr, Sub, PP, Sub, PP),
    INST("mov_sv_app", 0xD4B4, At("ArRn1", 1), At("ArStep1", 0), Const("Bx", 1), BSr, Sub, PP, Sub, PP),
    INST("mov_sv_app", 0x98E0, At("ArRn1", 4), At("ArStep1Alt", 3), At("Bx", 2), BSr, Sub, PP, Sub, PP),

    # <<< CBS >>>
    INST("cbs", 0x9068, At("Axh", 0), At("CbsCond", 8)),
    INST("cbs", 0xD49E, At("Axh", 8), At("Bxh", 5), At("CbsCond", 0)),
    INST("cbs", 0xD5C0, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), At("CbsCond", 3)),

    # [[[XXX_xy_XXX_xy_XXX]]]
    INST("mma", 0x4D88, AtNamed("Ax", 1), SX, SY, SX, SY, BZr, Add, PP, Sub, PP),
    INST("mma", 0xD49D, AtNamed("Bx", 5), SX, SY, SX, SY, BZr, Add, PP, Sub, PP),
    INST("mma", 0x5E24, AtNamed("Ab", 0), SX, SY, SX, SY, BZr, Add, PP, Add, PP),
    INST("mma", 0x8061, AtNamed("Ab", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PP),
    INST("mma", 0x8071, AtNamed("Ab", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PA),
    INST("mma", 0x8461, AtNamed("Ab", 8), SX, SY, SX, SY, BAc, Sub, PP, Sub, PP),
    INST("mma", 0x8471, AtNamed("Ab", 8), SX, SY, SX, SY, BAc, Sub, PP, Sub, PA),
    INST("mma", 0xD484, AtNamed("Ab", 0), SX, SY, SX, SY, BAc, Add, PA, Add, PA),
    INST("mma", 0xD4A0, AtNamed("Ab", 0), SX, SY, SX, SY, BAc, Add, PP, Sub, PP),
    INST("mma", 0x4D89, AtNamed("Ax", 1), SX, SY, SX, UY, BZr, Add, PP, Sub, PP),
    INST("mma", 0xD59D, AtNamed("Bx", 5), SX, SY, SX, UY, BZr, Add, PP, Sub, PP),
    INST("mma", 0x5F24, AtNamed("Ab", 0), SX, SY, SX, UY, BZr, Add, PP, Add, PP),
    INST("mma", 0x8069, AtNamed("Ab", 8), SX, SY, SX, UY, BAc, Add, PP, Add, PP),
    INST("mma", 0x8079, AtNamed("Ab", 8), SX, SY, SX, UY, BAc, Add, PP, Add, PA),
    INST("mma", 0x8469, AtNamed("Ab", 8), SX, SY, SX, UY, BAc, Sub, PP, Sub, PP),
    INST("mma", 0x8479, AtNamed("Ab", 8), SX, SY, SX, UY, BAc, Sub, PP, Sub, PA),
    INST("mma", 0xD584, AtNamed("Ab", 0), SX, SY, SX, UY, BAc, Add, PA, Add, PA),
    INST("mma", 0xD5A0, AtNamed("Ab", 0), SX, SY, SX, UY, BAc, Add, PP, Sub, PP),

    # [[[XXX_mm_XXX_mm_XXX]]]
    INST("mma", 0xCA00, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, UX, SY, BAc, Sub, PP, Sub, PA),
    INST("mma", 0xCA01, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, SX, UY, BAc, Sub, PP, Sub, PA),
    INST("mma", 0xCA02, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, UX, SY, BAc, Sub, PA, Sub, PA),
    INST("mma", 0xCA03, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, SX, UY, BAc, Sub, PA, Sub, PA),
    INST("mma", 0xCA04, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, UX, SY, BAc, Add, PP, Add, PA),
    INST("mma", 0xCA05, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, SX, UY, BAc, Add, PP, Add, PA),
    INST("mma", 0xCA06, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, UX, SY, BAc, Add, PA, Add, PA),
    INST("mma", 0xCA07, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), UX, SY, SX, UY, BAc, Add, PA, Add, PA),
    INST("mma", 0xCB00, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, UX, SY, BAc, Sub, PP, Sub, PP),
    INST("mma", 0xCB01, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, SX, UY, BAc, Sub, PP, Sub, PP),
    INST("mma", 0xCB02, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, UX, SY, BAc, Sub, PP, Sub, PA),
    INST("mma", 0xCB03, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, SX, UY, BAc, Sub, PP, Sub, PA),
    INST("mma", 0xCB04, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, UX, SY, BAc, Add, PP, Add, PP),
    INST("mma", 0xCB05, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, SX, UY, BAc, Add, PP, Add, PP),
    INST("mma", 0xCB06, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, UX, SY, BAc, Add, PP, Add, PA),
    INST("mma", 0xCB07, At("ArpRn1", 5), At("ArpStep1", 3), At("ArpStep1", 4), EMod, EMod, AtNamed("Ab", 6), SX, SY, SX, UY, BAc, Add, PP, Add, PA),

    INST("mma", 0x0D30, At("ArpRn1", 3), At("ArpStep1", 1), At("ArpStep1", 2), EMod, DMod, AtNamed("Ax", 0), SX, SY, SX, UY, BAc, Add, PP, Add, PA),
    INST("mma", 0x0D20, At("ArpRn1", 3), At("ArpStep1", 1), At("ArpStep1", 2), DMod, EMod, AtNamed("Ax", 0), SX, SY, SX, UY, BAc, Add, PP, Add, PA),
    INST("mma", 0x4B50, At("ArpRn1", 3), At("ArpStep1", 1), At("ArpStep1", 2), DMod, DMod, AtNamed("Ax", 0), SX, SY, SX, UY, BAc, Add, PP, Add, PA),

    INST("mma", 0x9861, At("ArpRn1", 4), At("ArpStep1", 2), At("ArpStep1", 3), EMod, DMod, AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PP),
    INST("mma", 0x9862, At("ArpRn1", 4), At("ArpStep1", 2), At("ArpStep1", 3), DMod, EMod, AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PP),
    INST("mma", 0x9863, At("ArpRn1", 4), At("ArpStep1", 2), At("ArpStep1", 3), DMod, DMod, AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PP),

    INST("mma", 0x98E1, At("ArpRn1", 4), At("ArpStep1", 2), At("ArpStep1", 3), EMod, DMod, AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PA),
    INST("mma", 0x98E2, At("ArpRn1", 4), At("ArpStep1", 2), At("ArpStep1", 3), DMod, EMod, AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PA),
    INST("mma", 0x98E3, At("ArpRn1", 4), At("ArpStep1", 2), At("ArpStep1", 3), DMod, DMod, AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PA),

    INST("mma", 0x80C8, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), EMod, EMod, AtNamed("Ab", 10), SX, SY, SX, SY, BAc, Add, PP, Sub, PP),
    INST("mma", 0x81C8, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), EMod, EMod, AtNamed("Ab", 10), SX, SY, SX, SY, BAc, Add, PP, Sub, PA),
    INST("mma", 0x82C8, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), EMod, EMod, AtNamed("Ab", 10), SX, SY, SX, SY, BZr, Add, PP, Add, PP),
    INST("mma", 0x83C8, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), EMod, EMod, AtNamed("Ab", 10), SX, SY, SX, SY, BZr, Add, PP, Add, PA),

    INST("mma", 0x80C2, At("ArpRn1", 0), At("ArpStep1", 8), At("ArpStep1", 9), EMod, EMod, AtNamed("Ab", 10), SX, SY, SX, SY, BAc, Add, PP, Add, PA),
    INST("mma", 0x49C8, At("ArpRn1", 2), At("ArpStep1", 0), At("ArpStep1", 1), EMod, EMod, AtNamed("Ab", 4), SX, SY, SX, SY, BAc, Sub, PP, Sub, PA),
    INST("mma", 0x00C0, At("ArpRn1", 3), At("ArpStep1", 1), At("ArpStep1", 2), EMod, EMod, AtNamed("Ab", 4), SX, SY, SX, SY, BZr, Add, PP, Sub, PP),
    INST("mma", 0x00C1, At("ArpRn1", 3), At("ArpStep1", 1), At("ArpStep1", 2), EMod, EMod, AtNamed("Ab", 4), SX, SY, SX, SY, BZr, Add, PP, Sub, PA),
    INST("mma", 0xD7A0, At("ArpRn1", 3), At("ArpStep1", 1), At("ArpStep1", 2), EMod, EMod, AtNamed("Ax", 4), SX, SY, SX, SY, BSv, Add, PP, Add, PP),
    INST("mma", 0xD7A1, At("ArpRn1", 3), At("ArpStep1", 1), At("ArpStep1", 2), EMod, EMod, AtNamed("Ax", 4), SX, SY, SX, SY, BSr, Add, PP, Add, PP),

    INST("mma", 0xC800, At("ArpRn2", 4), At("ArpStep2", 0), At("ArpStep2", 2), EMod, EMod, AtNamed("Ab", 6), SX, SY, SX, SY, BAc, Add, PP, Add, PP),
    INST("mma", 0xC900, At("ArpRn2", 4), At("ArpStep2", 0), At("ArpStep2", 2), EMod, EMod, AtNamed("Ab", 6), SX, SY, SX, SY, BAc, Sub, PP, Sub, PP),

    # [[[XXX_mx_XXX_xy_XXX]]]
    INST("mma_mx_xy", 0xD5E0, At("ArRn1", 1), At("ArStep1", 0), AtNamed("Ax", 3), SX, SY, SX, SY, BAc, Sub, PP, Sub, PP),
    INST("mma_mx_xy", 0xD5E4, At("ArRn1", 1), At("ArStep1", 0), AtNamed("Ax", 3), SX, SY, SX, SY, BAc, Add, PP, Add, PP),

    # [[[XXX_xy_XXX_mx_XXX]]]
    INST("mma_xy_mx", 0x8862, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Sub, PP, Sub, PP),
    INST("mma_xy_mx", 0x8A62, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PP),

    # [[[XXX_my_XXX_my_XXX]]]
    INST("mma_my_my", 0x4DA0, At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 4), SX, SY, SX, UY, BAc, Sub, PP, Sub, PP),
    INST("mma_my_my", 0x4DA1, At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 4), SX, SY, SX, UY, BAc, Sub, PP, Sub, PA),
    INST("mma_my_my", 0x4DA2, At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 4), SX, SY, SX, UY, BAc, Add, PP, Add, PP),
    INST("mma_my_my", 0x4DA3, At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 4), SX, SY, SX, UY, BAc, Add, PP, Add, PA),

    INST("mma_my_my", 0x94E0, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Sub, PP, Sub, PP),
    INST("mma_my_my", 0x94E1, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, UX, SY, BAc, Sub, PP, Sub, PP),
    INST("mma_my_my", 0x94E2, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Sub, PP, Sub, PA),
    INST("mma_my_my", 0x94E3, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, UX, SY, BAc, Sub, PP, Sub, PA),
    INST("mma_my_my", 0x94E4, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PP),
    INST("mma_my_my", 0x94E5, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, UX, SY, BAc, Add, PP, Add, PP),
    INST("mma_my_my", 0x94E6, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, SX, SY, BAc, Add, PP, Add, PA),
    INST("mma_my_my", 0x94E7, At("ArRn1", 4), At("ArStep1", 3), AtNamed("Ax", 8), SX, SY, UX, SY, BAc, Add, PP, Add, PA),

    # [[[XXX_xy_XXX_xy_XXX_mov]]]
    INST("mma_mov", 0x4FA0, At("Axh", 6), At("Bxh", 2), At("ArRn1", 1), At("ArStep1", 0), AtNamed("Ab", 3), SX, SY, SX, SY, BAc, Add, PP, Add, PP),
    INST("mma_mov", 0xD3A0, At("Axh", 6), At("Bxh", 2), At("ArRn1", 1), At("ArStep1", 0), AtNamed("Ab", 3), SX, SY, SX, SY, BAc, Add, PP, Sub, PP),
    INST("mma_mov", 0x80D0, At("Axh", 9), At("Bxh", 8), At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 10), SX, SY, SX, SY, BSv, Add, PP, Sub, PP),
    INST("mma_mov", 0x80D1, At("Axh", 9), At("Bxh", 8), At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 10), SX, SY, SX, SY, BSr, Add, PP, Sub, PP),
    INST("mma_mov", 0x80D2, At("Axh", 9), At("Bxh", 8), At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 10), SX, SY, SX, SY, BSv, Add, PP, Add, PP),
    INST("mma_mov", 0x80D3, At("Axh", 9), At("Bxh", 8), At("ArRn1", 3), At("ArStep1", 2), AtNamed("Ax", 10), SX, SY, SX, SY, BSr, Add, PP, Add, PP),
    INST("mma_mov", 0x5818, At("ArRn2", 7), At("ArStep1", 6), AtNamed("Ax", 0), SX, SY, SX, SY, BSv, Add, PP, Sub, PP),
    INST("mma_mov", 0x5838, At("ArRn2", 7), At("ArStep1", 6), AtNamed("Ax", 0), SX, SY, SX, SY, BSr, Add, PP, Sub, PP),

    INST("addhp", 0x90E0, At("ArRn2", 2), At("ArStep2", 0), At("Px", 4), At("Ax", 8)),
    
]

def set_bits(frm : int, to : int):
    return (0xFFFFFFFF >> (32 - (to - frm + 1))) << frm

def extract_bits(inp: int, frm : int, to : int):

    #print(f"1 {inp:x} {frm} {to}")
    mask = (0xFFFF >> (16 - (to - frm + 1)))
    inp = inp >> (frm)

    #print(f"2 {inp:x} {mask} {frm} {to}")
    return mask & inp

def print_operand_tokens():
    operand_set = set()
    operand_set_16 = set()
    for i in instr:
        #print(i.name)
        for op in i.args:
            if op.op_type != "At":
                continue
            if op.name == "op":
                continue

            signed = ""
            if op.name != "BankFlags" and op.name.endswith('s'):
                signed = " signed"
            if op.begin >=16:
                operand_set_16.add(f"    {op.name}_{op.begin} = ({op.begin-16},{op.end-16}){signed}")
                continue
            operand_set.add(f"    {op.name}_{op.begin} = ({op.begin},{op.end}){signed}")
            # :add    MemRn_0,Ax_8 is MemRn_0 & Ax_8 & op_0307=0x10 & op_
    
    for o in sorted(operand_set):
        print(o)
    print("")
    for o in sorted(operand_set_16):
        print(o)


def append_opcode_tokens():
    for ins in instr:
        #print(i.name)
        mask = 0
        for op in ins.args:
            if op.op_type == "At":
                mask |= set_bits(op.begin, op.end)

        start = -1
        prev_bit = 1
        end = -1
        base_op = ins.base
        for i in range(16):
            if mask & (1 << i) == 0:
                if prev_bit == 1:
                    start = i
                prev_bit = 0
                end = i
                continue
            # else:
            if prev_bit == 0:
                oper = Operand("At")
                oper.name = "op"
                oper.begin = start
                oper.end = end
                ins.args += (oper,)
                prev_bit = 1
        if prev_bit == 0:
            oper = Operand("At")
            oper.name = "op"
            oper.begin = start
            oper.end = end
            ins.args += (oper,)
            prev_bit = 1
            # :add    MemRn_0,Ax_8 is MemRn_0 & Ax_8 & op_0307=0x10 & op_0915=0x43 unimpl

def print_opcode_tokens():
    op_set = set()
    append_opcode_tokens()
    for i in instr:
        for op in i.args:
            if op.op_type != "At":
                continue
            if op.name != "op":
                continue
            token = f"op_{op.begin:02}{op.end:02}"
            op_set.add(f"   {token} = ({op.begin},{op.end})")

    for o in sorted(op_set):
        print(o) 

def print_slaspec_tokens():
    print("# TOKENS")
    print("define token teakop (16)")
    print("# opcodes")
    print_opcode_tokens()
    print("\n# operands")
    print_operand_tokens()
    print(";")

def print_attachments():
    opset = set()
    for i in instr:
        for op in i.args:
            if op.op_type != "At":
                continue
            if op.name == "op":
                continue

            opset.add(f"{op.name}_{op.begin}")

    prev_a = ''
    set_same_tok = set()
    attach_dict=dict()
    for t in sorted(opset):
        name = t.split("_")[0]
        if prev_a != name:
            # print(f"set_a={set_a}")
            attach_dict.update({name : set_same_tok.copy()})
            set_same_tok.clear()
            prev_a = name
        set_same_tok.add(t)

    attach_map = {
        "Ab": "b0 b1 a0 a1",
        "Abe" : "b0e b1e a0e a1e",
        "Abh" : "b0h b1h a0h a1h",
        "Abl" : "b0l b1l a0l a1l",
        "Ablh" : "b0l b0h b1l b1h a0l a0h a1l a1h",
        "ArArpSttMod" : "ar0 ar1 arp0 arp1 arp2 arp3 _ _ stt0 stt1 stt2 _ mod0 mod1 mod2 mod3",
        "ArArp" : "ar0 ar1 arp0 arp1 arp2 arp3 _ _",
        "Ar" : "ar0 ar1",
        "Arp" : "arp0 arp1 arp2 arp3",
        "Ax" : "a0 a1",
        "Axh" : "a0h a1h",
        "Axl" : "a0l a1l",
        "Bx" : "b0 b1",
        "Bxh" : "b0h b1h",
        "Px" : "p0 p1",
        "R0123" : "r0 r1 r2 r3",
        "R45" : "r4 r5",
        "RnOld" : "r0 r1 r2 r3 r4 r5 r7 y0",
        "Rn" : "r0 r1 r2 r3 r4 r5 r6 r7",
        "SttMod" : "stt0 stt1 stt2 _ mod0 mod1 mod2 mod3",
        }
    for same_tok in attach_dict.values():
        att_str = ""
        att_str += "attach variables [ "
        for t in sorted(same_tok):
            att_str += t + " "
        att_str += "]"

        mp = attach_map.get(t.split("_")[0], "")

        if mp != "":
            att_str += (f" [ {mp} ];")
        else:
            att_str = "# " + att_str
        
        print(att_str)

def write_sinc():
    append_opcode_tokens()
    # :add    MemRn_0,Ax_8 is MemRn_0 & Ax_8 & op_0307=0x10 & op_0915=0x43 unimpl

    for i in instr:
        mnemonic = i.name + "    "
        for op in i.args:
            if op.op_type != "At":
                continue
            if op.name == "op":
                continue

            opset.add(f"{op.name}_{op.begin}")



#print_slaspec_tokens()
print_attachments()

#    operand_set.add(f"    {op.name}_{op.begin} = ({op.begin},{op.end}){signed}")
