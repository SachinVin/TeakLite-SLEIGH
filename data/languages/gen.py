



with open('opcodes.txt', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        
        sp = line.split()
        print(sp)
        try:
            print(int(sp[0][:4], 16))
        except:
            print("pass...")
        