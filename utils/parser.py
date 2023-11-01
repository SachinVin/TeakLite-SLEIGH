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

    "Ab": 2,
    "Abl": 2,
    "Abh": 2,
    "Abe": 2,
    "R0123": 2,
    "R0425": 2,
    "R4567": 2,
    "Arp": 2,

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
            [operand, start] = s.split('@')
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
                to = int(s2)+1
                mask |= set_bits(int(s2), int(to))
                token = f"{operand}_{start}"
                op_mnemonic += (f"{token},")
                expanded_tokens_prefix = ("( ")
                expanded_tokens.append(f") ... & {token}") # todo: open bracket ..
                token1 = f"{operand}_{s1}"
                token2 = f"{operand}_{s2}"
                tok_set.add(f"{token1} = ({s1},{int(s1)+16})")
                tok_set.add(f"{token2} = ({s2},{int(s2)+2})")
                continue
            if (length == 0):
                length = int(start)
                print(f"Unhandled: {s}")

            to = int(start)+length-1
            mask |= set_bits(int(start), int(to))
            token = f"{operand}_{start}"
            if(int(start) > 15):
                expanded_tokens.append(f"; {token}")
            else:
                op_constructor.append(token)
            op_mnemonic += (f"{token},")
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
        
        outf.write("{ }\n\n")

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


#print_ops()