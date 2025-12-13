#[0, 3, 0, 5] -> {1: 3, 3: 5}
def createSparseVector(values):
    result = {}
    for i in range(len(values)):
        if values[i] != 0:
            result[i] = values[i]
    return result

#{1: 3, 3: 5}
#index = 1 -> 3
def getElement(sparseVec, index):
    if index in sparseVec:
        return sparseVec[index]
    return 0

#{1: 3, 3: 5}
#sparseVec, 1, 0 -> {3: 5}
#sparseVec, 2, 7 - > {3: 5, 2: 7}
def setElement(sparseVec, index, value):
    if value == 0:
        if index in sparseVec:
            del sparseVec[index]
    else:
        sparseVec[index] = value


#vec1 = {1: 3, 3: 5}
#vec2 = {1: 2, 2: 4}
#{1: 5, 3: 5, 2: 4}
def addVectors(vec1, vec2):
    result = {}
    for idx in vec1: 
        result[idx] = vec1[idx]
    for idx in vec2: 
        if idx in result:
            result[idx] = result[idx] + vec2[idx]
        else:
            result[idx] = vec2[idx] 
    toRemove = []
    for idx in result:
        if result[idx] == 0:
            toRemove.append(idx)
    for idx in toRemove:
        del result[idx]
    return result

#vec1 = {1: 3, 3: 5 2: 5}
#vec2 = {1: 2, 3: 4}
#3*2 + 5*4 + 0 = 6 + 20 = 26
def dotProduct(vec1, vec2):
    result = 0
    for idx in vec1:
        if idx in vec2:
            result = result + vec1[idx] * vec2[idx]
    return result

#vec = {1: 3, 2: 5}
#{1: 6, 2: 10}
def scaleVector(vec, scalar):
    result = {}
    for idx in vec:
        result[idx] = vec[idx] * scalar
    return result

#vec = {1: 3, 2: 4}
# srt 25 = 5
def vectorLength(vec):
    sumSquares = 0
    for idx in vec:
        sumSquares = sumSquares + vec[idx] * vec[idx]
    length = sumSquares ** 0.5
    return length

#vec1 = {1: 3, 2: 4}
#vec2 = {1: 2, 2: 4}
#0.9839
def cosineSimilarity(vec1, vec2):
    dot = dotProduct(vec1, vec2)
    len1 = vectorLength(vec1)
    len2 = vectorLength(vec2)
    if len1 == 0 or len2 == 0:
        return 0
    return dot / (len1 * len2)

#sparseVec = {1: 3, 3: 5}
#sparseVec, 5
#[0, 3, 0, 5, 0]
def toDense(sparseVec, size):
    result = []
    for i in range(size):
        result.append(getElement(sparseVec, i))
    return result

#{1: 3, 3: 5} - > 2
def countNonZero(sparseVec):
    return len(sparseVec)

#{1: 3, 3: 5} -> 2*16 = 32 bait
def getMemorySize(sparseVec):
    return len(sparseVec) * 16
