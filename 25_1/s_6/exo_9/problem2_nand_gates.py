def nand(a, b):
    return 1 if not (a == 1 and b == 1) else 0


def not_gate(a):
    return nand(a, a)


def and_gate(a, b):
    return not_gate(nand(a, b))


def or_gate(a, b):
    not_a = not_gate(a)
    not_b = not_gate(b)
    return nand(not_a, not_b)


def start():
    print("NAND truth table:")
    print("A B | A NAND B")
    for a in [0, 1]:
        for b in [0, 1]:
            print(f"{a} {b} |    {nand(a, b)}")
    
    print("\n" + "="*50)
    print("NOT from NAND:")
    print("NOT(A) = A NAND A")
    print("\nA | NOT A")
    for a in [0, 1]:
        print(f"{a} |   {not_gate(a)}")
    
    print("\n" + "="*50)
    print("AND from NAND:")
    print("AND(A,B) = NOT(A NAND B) = (A NAND B) NAND (A NAND B)")
    print("\nA B | A AND B")
    for a in [0, 1]:
        for b in [0, 1]:
            print(f"{a} {b} |    {and_gate(a, b)}")
    
    print("\n" + "="*50)
    print("OR from NAND:")
    print("OR(A,B) = (NOT A) NAND (NOT B) = (A NAND A) NAND (B NAND B)")
    print("\nA B | A OR B")
    for a in [0, 1]:
        for b in [0, 1]:
            print(f"{a} {b} |   {or_gate(a, b)}")
    
    print("\n" + "="*50)
    print("Summary:")
    print("NOT(A) uses 1 NAND gate")
    print("AND(A,B) uses 2 NAND gates")
    print("OR(A,B) uses 3 NAND gates")
    print("total we can build any circuit with only NAND gates")


start()
