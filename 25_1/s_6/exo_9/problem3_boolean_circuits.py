def generate_all_inputs(n):
    result = []
    for i in range(2 ** n):
        bits = []
        for j in range(n):
            bits.append((i >> j) & 1)
        bits.reverse()
        result.append(bits)
    return result


def delta_function(x, target):
    if x == target:
        return 1
    return 0


def count_gates_for_delta(n):
    return n + 1


def build_circuit_size(n):
    all_inputs = generate_all_inputs(n)
    num_inputs = len(all_inputs)
    
    gates_per_delta = count_gates_for_delta(n)
    total_gates = num_inputs * gates_per_delta
    
    return total_gates


def start():
    print("problem Universality of Boolean Circuits")
    print("F: {0,1}^n -> {0,1}")
    print()
    
    for n in range(1, 6):
        all_inputs = generate_all_inputs(n)
        num_inputs = len(all_inputs)
        gates_per_delta = count_gates_for_delta(n)
        total_gates = build_circuit_size(n)
        
        print(f"n = {n}:")
        print(f"  number possible inputs: 2^{n} = {num_inputs}")
        print(f"  gates per delta function: O({n}) = ~{gates_per_delta}")
        print(f"  total gates needed: O(n * 2^n) = ~{total_gates}")
        print()
    
    print("="*50)
    print("example with n=2:")
    print()
    
    all_inputs = generate_all_inputs(2)
    print("all possible inputs:")
    for i in range(len(all_inputs)):
        print(f"  x{i} = {all_inputs[i]}")
    
    print()
    print("delta functions:")
    for i in range(len(all_inputs)):
        target = all_inputs[i]
        print(f"  delta_{target}(x) = 1 if x = {target}, else 0")
    
    print()
    print("any function F can be written as:")
    print("F(x) = OR of all delta_x where F(x) = 1")
    print()
    print("circuit size:")
    print(f"  each delta: O(n) = O(2) gates")
    print(f"  total deltas: 2^n = 4")
    print(f"  total size: O(n * 2^n) = O(2 * 4) = O(8) gates")


start()
