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
outf = open('./teakra_opcodes.out.py', 'w')
with open('./teakra_opcodes.txt', 'r') as f:
    for l in f:
        line:str = l.strip()
        if line.startswith('///'):
            outf.write('    ##'+line[3:]+"\n")
            continue
        if line.startswith('//'):
            outf.write('    #'+line[2:]+"\n")
            continue
        if line == '':
            outf.write("\n")
            continue

        tmp = ""
        if line.startswith('INST'):
            mn_beg = 5
            mn_end = line.find(",")
            tmp = line[:mn_beg] + '"' +line[mn_beg:mn_end] + '"' + line[mn_end:]
            pass
        if line.startswith('.EXCEPT'):
            tmp = "    "+line
            pass
        

        at_beg = tmp.find("<")
        while at_beg != -1:
            at_beg += 1
            at_end = tmp.find(",",at_beg)
            #print(f"at_beg={at_beg} at_end={at_end}")
            #print(tmp[at_beg-7:at_beg])
            if ("Unused<" != tmp[at_beg-7:at_beg]):
                tmp = tmp[:at_beg] + '"' +tmp[at_beg:at_end] + '"' + tmp[at_end:]
            #print(f"{tmp}\n")
            at_beg = tmp.find("<", at_end)

        tmp = tmp.replace("<", "(").replace(">", ")")
        tmp = tmp.replace("//", "#")
        outf.write("    "+tmp+"\n")


outf.close()






