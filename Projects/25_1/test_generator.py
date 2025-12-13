# just random
def randomNumber(seed, minVal, maxVal):
    seed = (seed * 9301 + 49297) % 233280
    return minVal + (seed / 233280.0) * (maxVal - minVal), seed

#vector = {}
#  randomNumber(seed, 0, 1): if > sparsity(80% null)  ->  {1: -23, 3: 45}
def generateRandomVector(size, sparsity, seed):
    vector = {}
    for i in range(size):
        rand, seed = randomNumber(seed, 0, 1)
        if rand > sparsity:
            value, seed = randomNumber(seed, -100, 100)
            vector[i] = value
    return vector, seed


#denseMatrix = [] row = [](null)
#randomNumber(seed, 0, 1) for each col
'''
[
    [0, 0, 57, 0],
    [-23, 0, 0, 45],
    [0, 0, 0, 3]
]
'''
def generateRandomMatrix(rows, cols, sparsity, seed):
    denseMatrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            rand, seed = randomNumber(seed, 0, 1)
            if rand > sparsity:
                value, seed = randomNumber(seed, -100, 100)
                row.append(value)
            else:
                row.append(0)
        denseMatrix.append(row)
    return denseMatrix, seed




def generateTestCases():
    testCases = [
        {'size': 100, 'sparsity': 0.9, 'name': 'small 90% sparse'},
        {'size': 100, 'sparsity': 0.95, 'name': 'small 95% sparse'},
        {'size': 100, 'sparsity': 0.99, 'name': 'small 99% sparse'},
        {'size': 500, 'sparsity': 0.9, 'name': 'medium 90% sparse'},
        {'size': 500, 'sparsity': 0.95, 'name': 'medium 95% sparse'},
        {'size': 500, 'sparsity': 0.99, 'name': 'medium 99% sparse'},
        {'size': 1000, 'sparsity': 0.9, 'name': 'large 90% sparse'},
        {'size': 1000, 'sparsity': 0.95, 'name': 'large 95% sparse'},
        {'size': 1000, 'sparsity': 0.99, 'name': 'large 99% sparse'},
        {'size': 2000, 'sparsity': 0.95, 'name': 'big 95% sparse'},
        {'size': 2000, 'sparsity': 0.99, 'name': 'big 99% sparse'},
    ]
    return testCases


# nonZero = len(vec) - how many 0
# vec = {1: 3, 3: 5} -> My Vector:  Non-zero elements: 2  Memory: 32 bytes
def printVectorInfo(vec, name):
    nonZero = len(vec)
    print(f"{name}:")
    print(f"  how many non zero elements is {nonZero}")
    print(f"  memory is {nonZero * 16} byt")



# countNonZeroMatrix(matrix) -how many non 0
'''
matrix = {
    'rows': 3,
    'cols': 3,
    'data': [5, 1],
    'colIndex': [0, 1],
    'rowPtr': [0, 1, 2, 2]
}

printMatrixInfo(matrix, "My Matrix")

My Matrix:
  size is 3x3
  total elements 9
  non zero is 2
  sparsity is 77.78%
  memory is 40 byt (0.04 KB)
'''
def printMatrixInfo(matrix, name):
    from SparseMatrix import countNonZeroMatrix, getMemorySizeMatrix, getSparsity
    nonZero = countNonZeroMatrix(matrix)
    memory = getMemorySizeMatrix(matrix)
    sparsity = getSparsity(matrix)
    totalElements = matrix['rows'] * matrix['cols']
    print(f"{name}:")
    print(f"  size is {matrix['rows']}x{matrix['cols']}")
    print(f"  total elements {totalElements}")
    print(f"  non zero is {nonZero}")
    print(f"  sparsity is {sparsity*100:.2f}%")
    print(f"  memory is {memory} byt ({memory/1024:.2f} KB)")
