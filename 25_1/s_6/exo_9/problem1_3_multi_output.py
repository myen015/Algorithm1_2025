def count_functions(n, m):
    inputs = 2 ** n
    outputs = 2 ** m
    total = outputs ** inputs
    return total

def start():
    print("problem count functions F: {0,1}^n -> {0,1}^m")
    print()
    
    for n in range(1, 4):
        for m in range(1, 4):
            inputs = 2 ** n
            outputs = 2 ** m
            result = count_functions(n, m)
            print(f"n = {n}, m = {m}:")
            print(f"  number inputs: 2^{n} = {inputs}")
            print(f"  number outputs: 2^{m} = {outputs}")
            print(f"  number functions: 2^(m*2^{n}) = {outputs}^{inputs} = {result}")
            print()
    
    print("Formula: 2^(m * 2^n)")

start()
