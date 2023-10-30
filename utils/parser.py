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
    if operand.startswith("Mem"):
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

    length = token_len_map.get(operand, 0)
    return length


tok_set=set()
with open('./opcodes.txt', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        if line.strip().startswith('||'):
            continue
        sp = line.split()
        #print(sp)
        base_op = int(sp[0][:4], 16)
        #print(base_op)
        if len(sp) < 3:
            print("wut...")
            continue
        
        for s in sp:
            if s.startswith('||'):
                break
            s=s.strip(',')
            #print(s)
            if s.find('@') >= 0 :
                [operand, start] = s.split('@')
                length = get_tok_len(operand)

                if (start.find('not')) != -1:
                    start = start.strip('not')
                    tok_set.add(f"{operand}_not{start} = ({start},{int(start)+length-1})")
                    continue
                if (start.find('and')) != -1:
                    # eg Address18@16and5
                    [s1, s2] = start.split('and')
                    if s1 != '16':
                        print(f"Unknown s={s}")
                        continue
                    tok_set.add(f"{operand}_{s1} = ({s1},{int(s1)+16})")
                    tok_set.add(f"{operand}_{s2} = ({s2},{int(s2)+2})")
                    continue
                if (length == 0):
                    length = int(start)
                    print("Unhandled")
                tok_set.add(f"{operand}_{start} = ({start},{int(start)+length-1})")
                continue


        
for t in sorted(tok_set):
    print(f"    {t}")
        