# MASTER THEOREM COMPLEXITY ANALYSIS

## RECURRENCE RELATION

T(n) = T(n/2) + O(1)

## PARAMETERS FOR MASTER THEOREM

a = 1
b = 2
f(n) = O(1), so d = 0

## MASTER THEOREM CASE

log_b(a) = log_2(1) = 0

d = log_b(a) = 0

## CASE 2: When d = log_b(a)

T(n) = Θ(n^(log*b(a)) * log n)
T(n) = Θ(n^0 \_ log n)
T(n) = Θ(log n)

THEREFORE: T(n) = O(log n)

## WHY LOG_2(N)

Binary exponentiation divides the exponent by 2 at each recursion level:

n → n/2 → n/4 → n/8 → ... → 1

Number of levels = log_2(n)

Each level performs one 2x2 matrix multiplication = O(1)

Total time = number of levels × work per level = log_2(n) × O(1) = O(log n)
