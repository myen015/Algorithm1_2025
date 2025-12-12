
# -----------------------------------------------------------
# Part 1: Finite functions 
# -----------------------------------------------------------

def all_boolean_vectors(n):
    """Generate all 0/1 vectors of length n."""
    res = []
    def gen(i, cur):
        if i == n:
            res.append(cur[:])
            return
        cur.append(0)
        gen(i+1, cur)
        cur.pop()
        cur.append(1)
        gen(i+1, cur)
        cur.pop()
    gen(0, [])
    return res


# -----------------------------------------------------------
# Part 2: NAND-based logic gates
# -----------------------------------------------------------

def NAND(a, b):
    return 0 if (a and b) else 1


def NOT(x):
    return NAND(x, x)


def AND(a, b):
    t = NAND(a, b)
    return NAND(t, t)


def OR(a, b):
    return NAND(NOT(a), NOT(b))


# -----------------------------------------------------------
# Part 3: Build δ_x(y) (Kronecker indicator)
# δ_x(y) = 1 if y == x, else 0
# -----------------------------------------------------------

def delta_x(x, y):
    """
    Compute δ_x(y) = 1 if y == x else 0,
    using only AND and NOT (which internally use NAND).
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same dimension")

    bits = []
    for xi, yi in zip(x, y):
        if xi == 1:
            bits.append(yi)         # literal y_i
        else:
            bits.append(NOT(yi))    # literal ¬y_i

    # Compute AND of all bits (sequential)
    out = 1
    for b in bits:
        out = AND(out, b)

    return out


# -----------------------------------------------------------
# Part 4: Evaluate F(y) = OR_{x : F(x)=1} delta_x(y)
# F is given as a dictionary: tuple(x) -> 0/1
# -----------------------------------------------------------

def build_F_function(F_table):
    """
    Construct F(y) using the DNF-like expansion:
    F(y) = OR( delta_x1(y), delta_x2(y), ... )

    F_table is a dict mapping tuples x -> 0/1.
    """
    xs = [list(k) for k, v in F_table.items() if v == 1]

    def F_eval(y):
        out = 0
        for x in xs:
            out = OR(out, delta_x(x, y))
        return out

    return F_eval


# -----------------------------------------------------------
# Small test
# -----------------------------------------------------------

if __name__ == "__main__":
    # Example: n = 2 function table
    # F(00)=0, F(01)=1, F(10)=1, F(11)=0
    F_table = {
        (0,0): 0,
        (0,1): 1,
        (1,0): 1,
        (1,1): 0
    }

    F = build_F_function(F_table)

    print("Testing F(y) via NAND-based circuit:")
    for vec in all_boolean_vectors(2):
        print(vec, "->", F(vec))
