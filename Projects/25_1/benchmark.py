import time
import SparseVector as sv
import SparseMatrix as sm
import test_generator as tg

try:
    import scipy.sparse as sp
    import numpy as np
    SCIPY_AVAILABLE = True
except:
    SCIPY_AVAILABLE = False
    print("scipy not available - only testing custom implementation")

try:
    import matplotlib.pyplot as plt
    PLOT_AVAILABLE = True
except:
    PLOT_AVAILABLE = False
    print("matplotlib not available - no plots")

def test_vector_speed():
    print("\n=== VECTOR SPEED TEST ===\n")
    
    # it is size of vectors
    sizes = [100, 500, 1000, 2000, 5000]
    sparsity = 0.95
    
    # just to save result
    results = {
        'sizes': [],
        'custom_create': [],
        'custom_dot': [],
        'custom_add': [],
        'scipy_create': [],
        'scipy_dot': [],
        'scipy_add': [],
    }
    
    seed = 12345
    
    for size in sizes:
        print(f"\nTesting size: {size}")
        results['sizes'].append(size)
        
        vec1, seed = tg.generateRandomVector(size, sparsity, seed) # we generate evector
        vec2, seed = tg.generateRandomVector(size, sparsity, seed)
        
        # tim to cretaing vector
        start = time.time()
        customVec1 = vec1
        customVec2 = vec2
        customTime = time.time() - start
        results['custom_create'].append(customTime * 1000)
        print(f"  Custom create: {customTime*1000:.4f} ms")
        
        # time to product
        start = time.time()
        result = sv.dotProduct(customVec1, customVec2)
        customTime = time.time() - start
        results['custom_dot'].append(customTime * 1000)
        print(f"  custom dot product {customTime*1000:.4f} ms")
        
        #time to add
        start = time.time()
        result = sv.addVectors(customVec1, customVec2)
        customTime = time.time() - start
        results['custom_add'].append(customTime * 1000)
        print(f"  custom add {customTime*1000:.4f} ms")
        
        if SCIPY_AVAILABLE:
            dense1 = sv.toDense(vec1, size) # creating vector разрежённые векторы в плотные
            dense2 = sv.toDense(vec2, size)
            
            start = time.time()
            scipyVec1 = sp.csr_matrix([dense1]) # преобразуем плотный вектор в CSR формат
            scipyVec2 = sp.csr_matrix([dense2])
            scipyTime = time.time() - start
            results['scipy_create'].append(scipyTime * 1000)
            print(f"  Scipy create: {scipyTime*1000:.4f} ms")
            
            start = time.time()
            result = scipyVec1.dot(scipyVec2.T)
            scipyTime = time.time() - start
            results['scipy_dot'].append(scipyTime * 1000)
            print(f"  Scipy dot product: {scipyTime*1000:.4f} ms")
            
            start = time.time()
            result = scipyVec1 + scipyVec2
            scipyTime = time.time() - start
            results['scipy_add'].append(scipyTime * 1000)
            print(f"  Scipy add: {scipyTime*1000:.4f} ms")
    
    return results

def test_matrix_speed():
    print("\n=== MATRIX SPEED TEST ===\n")
    
    sizes = [50, 100, 200, 500]
    sparsity = 0.95
    
    results = {
        'sizes': [],
        'custom_create': [],
        'custom_matvec': [],
        'scipy_create': [],
        'scipy_matvec': [],
    }
    
    seed = 54321
    
    for size in sizes:
        print(f"\nTesting size: {size}x{size}")
        results['sizes'].append(size)
        
        denseMatrix, seed = tg.generateRandomMatrix(size, size, sparsity, seed)
        vec, seed = tg.generateRandomVector(size, sparsity, seed)
        
        start = time.time()
        customMatrix = sm.fromDenseMatrix(denseMatrix)
        customTime = time.time() - start
        results['custom_create'].append(customTime * 1000)
        print(f"  Custom create: {customTime*1000:.4f} ms")
        
        start = time.time()
        result = sm.multiplyMatrixVector(customMatrix, vec)
        customTime = time.time() - start
        results['custom_matvec'].append(customTime * 1000)
        print(f"  Custom mat*vec: {customTime*1000:.4f} ms")
        
        if SCIPY_AVAILABLE:
            start = time.time()
            scipyMatrix = sp.csr_matrix(denseMatrix)
            scipyTime = time.time() - start
            results['scipy_create'].append(scipyTime * 1000)
            print(f"  Scipy create: {scipyTime*1000:.4f} ms")
            
            denseVec = sv.toDense(vec, size)
            start = time.time()
            result = scipyMatrix.dot(denseVec)
            scipyTime = time.time() - start
            results['scipy_matvec'].append(scipyTime * 1000)
            print(f"  Scipy mat*vec: {scipyTime*1000:.4f} ms")
    
    return results

def test_memory():
    print("\n=== MEMORY TEST ===\n")
    
    sizes = [100, 500, 1000, 2000]
    sparsities = [0.9, 0.95, 0.99]
    
    results = {
        'sizes': sizes,
        'sparsities': sparsities,
        'data': []
    }
    
    seed = 99999
    
    for sparsity in sparsities:
        sparseMemory = []
        denseMemory = []
        
        for size in sizes:
            denseMatrix, seed = tg.generateRandomMatrix(size, size, sparsity, seed)
            sparseMatrix = sm.fromDenseMatrix(denseMatrix)
            
            sparseMem = sm.getMemorySizeMatrix(sparseMatrix)
            sparseMemory.append(sparseMem / 1024)
            
            denseMem = size * size * 8
            denseMemory.append(denseMem / 1024)
            
            print(f"Size {size}x{size}, Sparsity {sparsity*100}%:")
            print(f"  Sparse: {sparseMem/1024:.2f} KB")
            print(f"  Dense: {denseMem/1024:.2f} KB")
            print(f"  Ratio: {(sparseMem/denseMem)*100:.2f}%")
        
        results['data'].append({
            'sparsity': sparsity,
            'sparse': sparseMemory,
            'dense': denseMemory
        })
    
    return results

def make_plots(vectorResults, matrixResults, memoryResults):
    if not PLOT_AVAILABLE:
        print("\nno matplotlib")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Sparse Vector and Matrix Benchmarks', fontsize=16)
    axes[0, 0].plot(vectorResults['sizes'], vectorResults['custom_dot'], 'b-o', label='Custom')
    if SCIPY_AVAILABLE:
        axes[0, 0].plot(vectorResults['sizes'], vectorResults['scipy_dot'], 'r-s', label='Scipy')
    axes[0, 0].set_xlabel('Vector Size')
    axes[0, 0].set_ylabel('Time (ms)')
    axes[0, 0].set_title('Dot Product Performance')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Vector addition
    axes[0, 1].plot(vectorResults['sizes'], vectorResults['custom_add'], 'b-o', label='Custom')
    if SCIPY_AVAILABLE:
        axes[0, 1].plot(vectorResults['sizes'], vectorResults['scipy_add'], 'r-s', label='Scipy')
    axes[0, 1].set_xlabel('Vector Size')
    axes[0, 1].set_ylabel('Time (ms)')
    axes[0, 1].set_title('Vector Addition Performance')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    axes[1, 0].plot(matrixResults['sizes'], matrixResults['custom_matvec'], 'b-o', label='Custom')
    if SCIPY_AVAILABLE:
        axes[1, 0].plot(matrixResults['sizes'], matrixResults['scipy_matvec'], 'r-s', label='Scipy')
    axes[1, 0].set_xlabel('Matrix Size (NxN)')
    axes[1, 0].set_ylabel('Time (ms)')
    axes[1, 0].set_title('Matrix-Vector Multiplication Performance')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    for data in memoryResults['data']:
        sparsity = data['sparsity']
        axes[1, 1].plot(memoryResults['sizes'], data['sparse'], 'o-', 
                       label=f'Sparse {sparsity*100}%')
    axes[1, 1].plot(memoryResults['sizes'], memoryResults['data'][0]['dense'], 'r--', 
                   label='Dense', linewidth=2)
    axes[1, 1].set_xlabel('Matrix Size (NxN)')
    axes[1, 1].set_ylabel('Memory (KB)')
    axes[1, 1].set_title('Memory Usage Comparison')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    print("\nsaved as benchmark_results.png")
    plt.show()

print("=" * 60)
print("SPARSE LIBRARY BENCHMARK")
print("Custom vs scipy.sparse")
print("=" * 60)

vectorResults = test_vector_speed()
matrixResults = test_matrix_speed()
memoryResults = test_memory()

make_plots(vectorResults, matrixResults, memoryResults)

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
