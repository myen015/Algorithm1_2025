def fib(n):
	def mult(a, b):
		return [
			[a[0][0]*b[0][0]+a[0][1]*b[1][0], a[0][0]*b[0][1]+a[0][1]*b[1][1]],
			[a[1][0]*b[0][0]+a[1][1]*b[1][0], a[1][0]*b[0][1]+a[1][1]*b[1][1]]
		]
	def pow(m, k):                      # fast exponentiation of a 2x2 matrix
		if k == 1: return m
		if k % 2 == 0:
			tmp = pow(m, k//2)          # each matrix multiply here is - O(1), because multiplying two 2x2 matrices always takes the same small number of multiplication
			return mult(tmp, tmp)
		else:
			return mult(m, pow(m, k-1)) #same heree - O(1)
	if n == 0: return 0
	mat = [[1,1],[1,0]]
	r = pow(mat, n-1)
	return r[0][0]

# due to the recurrence to time is T(n) = T(n/2) + O(1), mester theorem gives us T(n) = O(log2 (n))(because at each step we divide the problem size by 2)


print("Problem 1")
n = int(input("Enter 'n': "))
print("Fib(", n, ") =", fib(n))