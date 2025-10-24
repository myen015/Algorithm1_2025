print("Problem 3")

import random, math

def gen_vecs(cnt, N):   # for generating randiom 100 vectors
	vecs = []
	for i in range(cnt):
		v = [random.randint(0,1) for _ in range(N)]
		vecs.append(v)
	return vecs

def sim(x, y):          # 1st formula from exo3
	num = sum([x[i]*y[i] for i in range(len(x))])
	nx = sum(x)
	ny = sum(y)
	if nx*ny == 0: return 0
	return num / (nx * ny)

def jacc(x, y):         # 2nd formula from exo3
	inter = sum([1 for i in range(len(x)) if x[i]==y[i]==1])
	union = sum([1 for i in range(len(x)) if x[i]==1 or y[i]==1])
	return inter/union if union else 0
# they both measure how close two binary vectors and if we compute many similarities the values form a Gaussian-like distribution


# 100 vectors of N length
N = 20
vecs = gen_vecs(100, N)

sims = []
for i in range(len(vecs)-1):
	sims.append(sim(vecs[i], vecs[i+1]))

print("Average sim is approximately:", sum(sims)/len(sims))

# repeating while having big N because when N increases, the distribution of similarities becomes more concentrated forming a Gaussian shape.
N2 = 200
vecs2 = gen_vecs(100, N2)
s2 = []
for i in range(len(vecs2)-1):
	s2.append(sim(vecs2[i], vecs2[i+1]))

print("Average sim for larger N is approximately:", sum(s2)/len(s2))


# for w=5 and N=2000, their quantity of vectors:

Nbig, w = 2000, 5       # the number of possible vectors is the number of ways to choose 5 positions out of 2000
def comb(n, k):
	r = math.comb(n, k)
	return r
print("Possible sparse vectors =", comb(Nbig, w))

# the capacity can be seen as the maximum number of vectors that can be stored or recognized without confusion