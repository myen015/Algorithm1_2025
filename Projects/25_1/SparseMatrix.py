#
#
def createSparseMatrix(rows, cols):
    matrix = {
        'rows': rows,
        'cols': cols,
        'data': [],
        'colIndex': [],
        'rowPtr': [0]
    }
    return matrix

"""
'rows': 3,
    'cols': 3,
    'data': [],
    'colIndex': [],
    'rowPtr': [0]
"""
"""
'rows': 3,
    'cols': 3,
    'data': [5],         
    'rowPtr': [0, 0, 0, 1]
"""
def setMatrixElement(matrix, row, col, value):
    dense = toDenseMatrix(matrix)
    dense[row][col] = value
    newMatrix = fromDenseMatrix(dense)
    matrix['data'] = newMatrix['data']
    matrix['colIndex'] = newMatrix['colIndex']
    matrix['rowPtr'] = newMatrix['rowPtr']


# 
# matrix, 1, 2 -> 5
# matrix, 0, 1 -> 0
def getMatrixElement(matrix, row, col):
    start = matrix['rowPtr'][row]
    end = matrix['rowPtr'][row + 1]
    for i in range(start, end):
        if matrix['colIndex'][i] == col:
            return matrix['data'][i]
    return 0


#matrix -> CSR
"""
 [0, 0, 5],
    [1, 0, 0],
    [0, 0, 0]
"""
"""
'rows': 3,
    'cols': 3,
    'data': [5, 1],
    'colIndex': [2, 0],
    'rowPtr': [0, 1, 2, 2]
"""
def fromDenseMatrix(denseMatrix):
    rows = len(denseMatrix)
    cols = len(denseMatrix[0]) if rows > 0 else 0
    matrix = createSparseMatrix(rows, cols)
    
    for i in range(rows):
        for j in range(cols):
            if denseMatrix[i][j] != 0:
                matrix['data'].append(denseMatrix[i][j])
                matrix['colIndex'].append(j)
        matrix['rowPtr'].append(len(matrix['data']))
    
    return matrix


"""
 'rows': 3,
    'cols': 3,
    'data': [5, 1],
    'colIndex': [2, 0],
    'rowPtr': [0, 1, 2, 2]
"""
"""
[[0, 0, 5], [1, 0, 0], [0, 0, 0]]
"""
def toDenseMatrix(matrix):
    result = []
    for i in range(matrix['rows']):
        row = []
        for j in range(matrix['cols']):
            row.append(getMatrixElement(matrix, i, j))
        result.append(row)
    return result


"""
    'rows': 3,
    'cols': 3,
    'data': [5, 1],
    'colIndex': [2, 0],
    'rowPtr': [0, 1, 2, 2]

    vector = {0: 2, 2: 3}
"""
"""
    {0: 15, 1: 2}
"""
def multiplyMatrixVector(matrix, vector):
    result = {}
    
    for i in range(matrix['rows']):
        rowSum = 0
        start = matrix['rowPtr'][i]
        end = matrix['rowPtr'][i + 1]
        
        for idx in range(start, end):
            col = matrix['colIndex'][idx]
            value = matrix['data'][idx]
            vecValue = 0
            if col in vector:
                vecValue = vector[col]
            rowSum = rowSum + value * vecValue
        
        if rowSum != 0:
            result[i] = rowSum
    
    return result



def multiplyMatrixMatrix(mat1, mat2):
    if mat1['cols'] != mat2['rows']:
        return None
    
    result = []
    for i in range(mat1['rows']):
        row = []
        for j in range(mat2['cols']):
            value = 0
            for k in range(mat1['cols']):
                v1 = getMatrixElement(mat1, i, k)
                v2 = getMatrixElement(mat2, k, j)
                value = value + v1 * v2
            row.append(value)
        result.append(row)
    
    return fromDenseMatrix(result)


"""
'rows': 2,
    'cols': 2,
    'data': [1, 2],
    'colIndex': [0, 1],
    'rowPtr': [0, 1, 2]
"""
"""
 'rows': 2,
    'cols': 2,
    'data': [3, 4],
    'colIndex': [0, 1],
    'rowPtr': [0, 1, 2]
"""
"""
{'rows': 2, 'cols': 2, 'data': [4, 6], 'colIndex': [0, 1], 'rowPtr': [0, 1, 2]}
"""
def addMatrices(mat1, mat2):
    if mat1['rows'] != mat2['rows'] or mat1['cols'] != mat2['cols']:
        return None
    
    dense1 = toDenseMatrix(mat1)
    dense2 = toDenseMatrix(mat2)
    result = []
    
    for i in range(mat1['rows']):
        row = []
        for j in range(mat1['cols']):
            row.append(dense1[i][j] + dense2[i][j])
        result.append(row)
    
    return fromDenseMatrix(result)


def transposeMatrix(matrix):
    dense = toDenseMatrix(matrix)
    result = []
    for j in range(matrix['cols']):
        row = []
        for i in range(matrix['rows']):
            row.append(dense[i][j])
        result.append(row)
    return fromDenseMatrix(result)


def countNonZeroMatrix(matrix):
    return len(matrix['data'])


"""
 'rows': 2,
    'cols': 2,
    'data': [1, 3],
    'colIndex': [0, 1],
    'rowPtr': [0, 1, 2]

    2 * 8 + 2 * 4 + 3 * 4 = 36
"""
def getMemorySizeMatrix(matrix):
    dataSize = len(matrix['data']) * 8
    colSize = len(matrix['colIndex']) * 4
    rowSize = len(matrix['rowPtr']) * 4
    return dataSize + colSize + rowSize


def getSparsity(matrix):
    totalElements = matrix['rows'] * matrix['cols']
    nonZeroElements = countNonZeroMatrix(matrix)
    if totalElements == 0:
        return 0
    return 1.0 - (nonZeroElements / totalElements)
