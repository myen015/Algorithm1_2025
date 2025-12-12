def count_functions(n):
    inputs = 2 ** n
    outputs = 2
    total = outputs ** inputs
    return total


def start():
    print("problem count functions F: {0,1}^n -> {0,1}")
    print()
    
    for n in range(1, 5):
        inputs = 2 ** n
        result = count_functions(n)
        print(f"n = {n}:")
        print(f"  number inputs 2^{n} = {inputs}")
        print(f"  number functions 2^(2^{n}) = 2^{inputs} = {result}")
        print()
    
    print("formula 2^(2^n)")

start()
