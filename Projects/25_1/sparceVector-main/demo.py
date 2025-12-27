import SparseVector as sv
import SparseMatrix as sm
import test_generator as tg

def test_vectors():
    print("\n=== VECTOR TESTS ===\n")
    
    dense1 = [0, 3, 0, 0, 5, 0, 7, 0, 0, 2]
    dense2 = [1, 0, 0, 4, 0, 6, 0, 0, 8, 0]
    
    vec1 = sv.createSparseVector(dense1)
    vec2 = sv.createSparseVector(dense2)
    
    print(f"Vector 1: {dense1}")
    print(f"Sparse representation: {vec1}")
    print(f"Non-zero elements: {sv.countNonZero(vec1)}")
    print(f"Memory: {sv.getMemorySize(vec1)} bytes\n")
    
    print(f"Vector 2: {dense2}")
    print(f"Sparse representation: {vec2}")
    print(f"Non-zero elements: {sv.countNonZero(vec2)}\n")
    
    print("Vector addition:")
    result = sv.addVectors(vec1, vec2)
    print(f"vec1 + vec2 = {result}")
    print(f"Dense: {sv.toDense(result, 10)}\n")
    
    print("Dot product:")
    dot = sv.dotProduct(vec1, vec2)
    print(f"vec1 · vec2 = {dot}\n")
    
    print("Cosine similarity:")
    similarity = sv.cosineSimilarity(vec1, vec2)
    print(f"similarity(vec1, vec2) = {similarity:.4f}\n")
    
    print("Scaling:")
    scaled = sv.scaleVector(vec1, 2)
    print(f"vec1 * 2 = {scaled}")
    print(f"Dense: {sv.toDense(scaled, 10)}\n")

def test_matrix():
    print("\n=== MATRIX TESTS ===\n")
    
    dense = [
        [0, 2, 0, 0],
        [3, 0, 0, 4],
        [0, 0, 5, 0],
        [0, 6, 0, 7]
    ]
    
    matrix = sm.fromDenseMatrix(dense)
    print("Dense matrix:")
    for row in dense:
        print(f"  {row}")
    print(f"\nSparse representation (CSR format):")
    print(f"  data: {matrix['data']}")
    print(f"  colIndex: {matrix['colIndex']}")
    print(f"  rowPtr: {matrix['rowPtr']}")
    print(f"  Non-zero elements: {sm.countNonZeroMatrix(matrix)}")
    print(f"  Sparsity: {sm.getSparsity(matrix)*100:.1f}%")
    print(f"  Memory: {sm.getMemorySizeMatrix(matrix)} bytes\n")
    
    print("Matrix-vector multiplication:")
    vec = {0: 1, 1: 2, 2: 3, 3: 4}
    print(f"Vector: {vec}")
    result = sm.multiplyMatrixVector(matrix, vec)
    print(f"Matrix * vector = {result}")
    print(f"Dense: {sv.toDense(result, 4)}\n")
    
    print("Matrix addition:")
    dense2 = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    matrix2 = sm.fromDenseMatrix(dense2)
    result = sm.addMatrices(matrix, matrix2)
    print("matrix + identity =")
    resultDense = sm.toDenseMatrix(result)
    for row in resultDense:
        print(f"  {row}")
    print()
    
    print("Matrix transpose:")
    transposed = sm.transposeMatrix(matrix)
    print("Transposed matrix:")
    transDense = sm.toDenseMatrix(transposed)
    for row in transDense:
        print(f"  {row}")

def check_memory():
    print("\n=== MEMORY CHECK ===\n")
    
    sizes = [100, 500, 1000]
    sparsity = 0.95
    seed = 12345
    
    for size in sizes:
        denseMatrix, seed = tg.generateRandomMatrix(size, size, sparsity, seed)
        sparseMatrix = sm.fromDenseMatrix(denseMatrix)
        
        denseMemory = size * size * 8
        sparseMemory = sm.getMemorySizeMatrix(sparseMatrix)
        ratio = (sparseMemory / denseMemory) * 100
        
        print(f"Matrix {size}x{size}:")
        print(f"  Dense:  {denseMemory/1024:.2f} KB")
        print(f"  Sparse: {sparseMemory/1024:.2f} KB")
        print(f"  Savings: {100-ratio:.1f}%")
        print(f"  Compression: {denseMemory/sparseMemory:.1f}x\n")

def test_big_data():
    print("\n=== BIG TEST ===\n")
    
    seed = 99999
    denseMatrix, seed = tg.generateRandomMatrix(2000, 2000, 0.99, seed)
    matrix = sm.fromDenseMatrix(denseMatrix)
    
    tg.printMatrixInfo(matrix, "Big Matrix")
    
    vec, seed = tg.generateRandomVector(2000, 0.99, seed)
    tg.printVectorInfo(vec, "Big Vector")
    
    import time
    start = time.time()
    result = sm.multiplyMatrixVector(matrix, vec)
    elapsed = time.time() - start
    
    print(f"result: {len(result)} non-zero")
    print(f"time: {elapsed*1000:.2f} ms")

print("=" * 60)
print("SPARSE VECTOR AND MATRIX LIBRARY")
print("=" * 60)

test_vectors()
test_matrix()
check_memory()
test_big_data()

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
