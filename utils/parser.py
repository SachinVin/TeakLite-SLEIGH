# token len in bits

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

    "Ab": 2,
    "Abl": 2,
    "Abh": 2,
    "Abe": 2,
    "R0123": 2,
    "R0425": 2,
    "R4567": 2,
    "Arp": 2,
    "offsZIDZ": 2,
    "stepZIDS": 2,
    "modrstepZIDS": 2,
    "stepII2D2S": 2,
    "stepII2D2S0": 2,
    "modrstepII2D2S0": 2,

    "Ablh": 3,
    "R0123457y0": 3,
    "Rn": 3,
    "ArArp": 3,
    "SttMod": 3,
    "MemRn": 3,

    "Cond": 4,
    "ArArpSttMod": 4,
    "SwapTypes4": 4,
    

    "Register": 5,
    "RegisterP0": 5,

    "BankFlags6": 6,
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
    if operand.startswith('Address'):
        operand = operand[7:]
        return int(operand)
    if operand.startswith('RelAddr'):
        operand = operand[7:]
        return int(operand)

    length = token_len_map.get(operand, 0)
    return length

def set_bits(frm : int, to : int):
    return (0xFFFFFFFF >> (32 - (to - frm + 1))) << frm

def extract_bits(inp: int, frm : int, to : int):

    #print(f"1 {inp:x} {frm} {to}")
    mask = (0xFFFF >> (16 - (to - frm + 1)))
    inp = inp >> (frm)

    #print(f"2 {inp:x} {mask} {frm} {to}")
    return mask & inp


op_set = set()
def populate_op_set(mask : int):
    start = -1
    prev_bit = 1
    end = -1
    for i in range(16):
        if mask & (1 << i) == 0:
            if prev_bit == 1:
                start = i
            prev_bit = 0
            end = i
            continue
        # else:
        if prev_bit == 0:
            extract_bits()
            op_set.add(f"op_{start:02}{end:02} = ({start},{end})")
            prev_bit = 1
    if prev_bit == 0:
        op_set.add(f"op_{start:02}{end:02} = ({start},{end})")
        prev_bit = 1

tok_set=set()
outf = open('./out.sinc', 'w')
with open('./opcodes.txt', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        if line.strip().startswith('||'):
            continue
        if line.strip() == '':
            continue
        sp = line.split()
        #print(sp)
        op_constructor = []
        op_mnemonic = ""
        base_op = int(sp[0][:4], 16)
        op_mnemonic += (f"{sp[2]}    ")
        #print(base_op)
        if len(sp) < 3:
            print("wut...")
            continue
        mask = 0
        expanded_tokens_prefix=""
        expanded_tokens=[]
        for s in sp:
            s=s.strip(',')
            #print(s)
            if s.find('||') >= 0 :
                break
            if s.find('@') < 0 :
                continue
            op_split = s.split('@')
            if len(op_split) == 4:
                # eg MemR0425@10_MemR0425@10offsZIDZ@5
                op_split = [op_split[0],op_split[2], op_split[3]]
            [operand, start] = op_split[:2]

            length = get_tok_len(operand)

            if (start.find('not')) != -1:
                start = start.strip('not')
                to = int(start)+length-1
                mask |=  set_bits(int(start), int(to))
                token = f"{operand}_not{start}"
                op_constructor.append(token)
                op_mnemonic += (f"{token},")
                tok_set.add(f"{token} = ({start},{to})")
                continue
            if (start.find('and')) != -1:
                # eg Address18@16and5
                [s1, s2] = start.split('and')
                if s1 != '16':
                    print(f"Unknown s={s}")
                    continue
                to2 = int(s2)+1
                mask |= set_bits(int(s2), int(to2))
                token = f"{operand}_{start}"
                op_mnemonic += (f"{token},")
                expanded_tokens_prefix = ("( ")
                expanded_tokens.append(f") ... & {token} ") # todo: open bracket ..
                token1 = f"{operand}_{s1}"
                token2 = f"{operand}_{s2}"
                tok_set.add(f"{token1} = ({s1},{int(s1)+15})")
                tok_set.add(f"{token2} = ({s2},{to2})")
                continue
            step_mnemonic = ""
            if (start.find('step')) != -1 or (start.find('offs')) != -1:
                # 8stepII2D2S0
                step = ""
                #print(f"start={start}")
                if (start.find('step')) != -1:
                    [start, step] = start.split('step')
                    step = f"step{step}"
                else:
                    [start, step] = start.split('offs')
                    step = f"offs{step}"
                token = ""
                if len(op_split) > 2:
                    step_start = op_split[2]
                    step_length = get_tok_len(step)
                    to = int(step_start)+step_length-1
                    mask |= set_bits(int(step_start), int(to))
                    token = f"{step}_{step_start}"
                    tok_set.add(f"{token} = ({step_start},{to})")
                else:
                    token = f"\"{step}\""
                step_mnemonic = f"{token}"
            if (length == 0):
                length = int(start)
                print(f"Unhandled: {s}")

            to = int(start)+length-1
            mask |= set_bits(int(start), int(to))
            token = f"{operand}_{start}"
            if(int(start) > 15):
                expanded_tokens.append(f"; {token} ")
            else:
                op_constructor.append(token)
            op_mnemonic += (f"{token},")
            if step_mnemonic != "":
                op_constructor.append(step_mnemonic)
                op_mnemonic += (f"{step_mnemonic},")
            tok_set.add(f"{token} = ({start},{to})")
            continue
        
        op_mnemonic = op_mnemonic.strip(',')
        #print(f"base_op={base_op:X},mask={mask:X}")
        #populate_op_set(mask)
        start = -1
        prev_bit = 1
        end = -1
        for i in range(16):
            if mask & (1 << i) == 0:
                if prev_bit == 1:
                    start = i
                prev_bit = 0
                end = i
                continue
            # else:
            if prev_bit == 0:
                bits=extract_bits(base_op, start, end)
                token = f"op_{start:02}{end:02}"
                op_constructor.append(f"{token}=0x{bits:X}")
                op_set.add(f"op_{start:02}{end:02} = ({start},{end})")
                prev_bit = 1
        if prev_bit == 0:
            bits=extract_bits(base_op, start, end)
            token = f"op_{start:02}{end:02}"
            op_constructor.append(f"{token}=0x{bits:X}")
            op_set.add(f"{token} = ({start},{end})")
            prev_bit = 1
        
        outf.write(f"# {line.strip().split('||')[0]}\n")
        #outf.write(f"# mask 0x{mask:04X}\n")
        outf.write(f":{op_mnemonic} is {expanded_tokens_prefix}",) 
        first = 1
        for op in op_constructor:
            if first:
                first = 0
            else:
                outf.write("& ")
            outf.write(f"{op} ")

        for e in expanded_tokens:
            outf.write(e)
        
        outf.write("unimpl\n\n")

sorted_tok_set = sorted(tok_set)

def print_operands():
    for t in sorted_tok_set:
        print(f"    {t}")

def print_attachments():
    prev_a = ''
    set_same_tok = set()
    attach_dict=dict()
    for t in sorted_tok_set:
        [a, b] = t.split('_')
        if prev_a != a:
            
            # print(f"set_a={set_a}")
            attach_dict.update({a : set_same_tok.copy()})
            set_same_tok.clear()
            prev_a = a
        set_same_tok.add(t.split('=')[0])

    for same_tok in attach_dict.values():
        print("attach variables [ ", end="") 
        for t in sorted(same_tok):
            print(f"{t}", end="")
        print("]") 

def print_ops():
    sorted_op_set = sorted(op_set)
    for o in sorted_op_set:
        print(f"    {o}")
    pass

def print_swap_types():
    swap_types_str = r'''
   val native           nocash         ;meaning
   0:  (a0,b0)          a0,b0          ;a0 <--> b0                ;flags(a0)
   1:  (a0,b1)          a0,b1          ;a0 <--> b1                ;flags(a0)
   2:  (a1,b0)          a1,b0          ;a1 <--> b0                ;flags(a1)
   3:  (a1,b1)          a1,b1          ;a1 <--> b1                ;flags(a1)
   4:  (a0,b0),(a1,b1)  a0:a1,b0:b1    ;a0 <--> b0 and a1 <--> b1 ;flags(a0)
   5:  (a0,b1),(a1,b0)  a0:a1,b1:b0    ;a0 <--> b1 and a1 <--> b0 ;flags(a0)
   6:  (a0,b0,a1)       a1,b0,a0       ;a0 --> b0 --> a1          ;flags(a1)
   7:  (a0,b1,a1)       a1,b1,a0       ;a0 --> b1 --> a1          ;flags(a1)
   8:  (a1,b0,a0)       a0,b0,a1       ;a1 --> b0 --> a0          ;flags(a0)
   9:  (a1,b1,a0)       a0,b1,a1       ;a1 --> b1 --> a0          ;flags(a0)
   A:  (b0,a0,b1)       b1,a0,b0       ;b0 --> a0 --> b1          ;flags(a0)!
   B:  (b0,a1,b1)       b1,a1,b0       ;b0 --> a1 --> b1          ;flags(a1)!
   C:  (b1,a0,b0)       b0,a0,b1       ;b1 --> a0 --> b0          ;flags(a0)!
   D:  (b1,a1,b0)       b0,a1,b1       ;b1 --> a1 --> b0          ;flags(a1)!
   E:  reserved         reserved       ;-                         ;-
   F:  reserved         reserved       ;-                         ;-
'''.split("\n")

    for s in swap_types_str:
        if s =="":
            continue
        sp = s.split()
        # SwapTypes4: "(a0,b0)"    is SwapTypes4_0=0    { local tmp:5 = a0; a0 = b0; b0 = tmp; }
        parms = sp[1].split(",")
        expr = ""
        regs = ""
        if len(parms) == 2:
            parms[0] = parms[0].strip("(")
            parms[1] = parms[1].strip(")")
            regs = f"{parms[0]} & {parms[1]}"
            expr = f"""
    local tmp:5 = {parms[0]};
    {parms[0]} = {parms[1]};
    {parms[1]} = tmp;
    # todo: update flags
"""
        if len(parms) == 3:
            parms[0] = parms[0].strip("(")
            #parms[1] = parms[1].strip(")")
            parms[2] = parms[2].strip(")")
            regs = f"{parms[0]} & {parms[1]} & {parms[2]}"
            expr = f"""
    local tmp:5 = {parms[2]};
    {parms[2]} = {parms[1]};
    {parms[1]} = {parms[0]};
    {parms[0]} = tmp;
    # todo: update flags
"""
        if len(parms) == 4:
            parms[0] = parms[0].strip("(")
            parms[1] = parms[1].strip(")")
            parms[2] = parms[2].strip("(")
            parms[3] = parms[3].strip(")")
            regs = f"{parms[0]} & {parms[1]} & {parms[2]} & {parms[3]}"
            expr = f"""
    local tmp:5 = {parms[0]};
    {parms[0]} = {parms[1]};
    {parms[1]} = tmp;
    tmp = {parms[2]};
    {parms[2]} = {parms[3]};
    {parms[3]} = tmp;
    # todo: update flags
"""

        print(f"SwapTypes4_0: {sp[1]}    is {regs} & SwapTypes4_0003=0x{sp[0][:1]}    \n{{{expr}}} ")

def print_status_reg_bitrange():
    stat_str = """
  0     LM   R/W Flag: Limit, set if saturation has/had occured    ;st0.5
  1     VL   R/W Flag: LatchedV, set if overflow has/had occurred  ;st0.5, too
  2     E    R/W Flag: Extension    ;see Cond e                    ;st0.6
  3     C    R/W Flag: Carry        ;see Cond c                    ;st0.7
  4     V    R/W Flag: Overflow     ;see Cond v                    ;st0.8
  5     N    R/W Flag: Normalized   ;see Cond nn                   ;st0.9
  6     M    R/W Flag: Minus        ;see Cond gt,ge,lt,le          ;st0.10
  7     Z    R/W Flag: Zero         ;see Cond eq,neq,gt,le         ;st0.11
  8-10  -    -   Unknown (reads as zero)
  11    C1   R/W Flag: Carry1 (2nd carry, for dual-operation opcodes)
  12-15 -    -   Unknown (reads as zero)
  """.split("\n")

    print("define bitrange ", end="")
    for s in stat_str:
        if s.strip() == '':
            continue
        sp = s.split()
        if sp[0].find('-') != -1:
            continue
             # a0l=a0[0,16]
        print(f"                {sp[1]}=stt0[{sp[0]},1]")
    
def print_cond():
    strn = """
0: true  ;Always                    ;always
1: eq    ;Equal to zero             ;Z=1
2: neq   ;Not equal to zero         ;Z=0
3: gt    ;Greater than zero         ;M=0 and Z=0
4: ge    ;Greater or equal to zero  ;M=0
5: lt    ;Less than zero            ;M=1
6: le    ;Less or equal to zero     ;M=1 or Z=1
7: nn    ;Normalize flag is cleared ;N=0
8: c     ;Carry flag is set         ;C=1
9: v     ;Overflow flag is set      ;V=1
A: e     ;Extension flag is set     ;E=1
B: l     ;Limit flag is set         ;L=1
C: nr    ;R flag is cleared         ;R=0
D: niu0  ;Input user pin 0 cleared  ;IUSER0=0
E: iu0   ;Input user pin 0 set      ;IUSER0=1
F: iu1   ;Input user pin 1 set      ;IUSER1=1
  """.split("\n")

    for s in strn:
        if s.strip() == '':
            continue
        sp = s.split()

        # thfcc: "eq"	is cond_full=0	{ local tmp:1 = (ZR!=0); export tmp; }
        cc= f"\"{sp[1]}\""
        sp2 = s.split(";")
        cond = sp2[2]
        cond_parm = cond.split("=")[0]
        print(f"Cond_0: {cc:8} is {cond_parm} & Cond_0003=0x{sp[0][0]} {{ local tmp:1 = ({cond}); export tmp; }} # {sp2[1]}")
    
#print_ops()
print_cond()
#print_swap_types()
#print_operands()
