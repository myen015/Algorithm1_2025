package main

import (
	"fmt"
	"math"
	"math/rand"
	"sort"
)

func generateBinaryVector(n int) []int {
	vec := make([]int, n)
	for i := 0; i < n; i++ {
		if rand.Float64() < 0.5 {
			vec[i] = 1
		}
	}
	return vec
}

func generateSparseBinaryVector(n, w int) []int {
	vec := make([]int, n)

	positions := rand.Perm(n)[:w]
	for _, pos := range positions {
		vec[pos] = 1
	}

	return vec
}

func dotProduct(x, y []int) int {
	sum := 0
	for i := range x {
		sum += x[i] * y[i]
	}
	return sum
}

func sum(x []int) int {
	s := 0
	for _, val := range x {
		s += val
	}
	return s
}

func maxElements(x, y []int) int {
	s := 0
	for i := range x {
		if x[i] > y[i] {
			s += x[i]
		} else {
			s += y[i]
		}
	}
	return s
}

func similarity(x, y []int) float64 {
	numerator := float64(dotProduct(x, y))
	denominator := float64(sum(x)) * float64(sum(y))

	if denominator == 0 {
		return 0
	}
	return numerator / denominator
}

func jaccard(x, y []int) float64 {
	intersection := float64(dotProduct(x, y))
	union := float64(maxElements(x, y))

	if union == 0 {
		return 0
	}
	return intersection / union
}

func computeStats(values []float64) (mean, stddev float64) {
	n := float64(len(values))
	sum := 0.0
	for _, v := range values {
		sum += v
	}
	mean = sum / n

	sumSq := 0.0
	for _, v := range values {
		diff := v - mean
		sumSq += diff * diff
	}
	stddev = math.Sqrt(sumSq / n)

	return mean, stddev
}

func binomial(n, k int) float64 {
	if k > n || k < 0 {
		return 0
	}
	if k == 0 || k == n {
		return 1
	}

	result := 1.0
	for i := 0; i < k; i++ {
		result *= float64(n - i)
		result /= float64(i + 1)
	}
	return result
}

func main() {
	rand.Seed(42) // For reproducibility

	fmt.Println("=== Problem 3: Neuro Computing ===\n")

	testSizes := []int{10, 50, 100, 200}

	for _, N := range testSizes {
		fmt.Printf("=== N = %d ===\n", N)

		numVectors := 100
		vectors := make([][]int, numVectors)
		for i := 0; i < numVectors; i++ {
			vectors[i] = generateBinaryVector(N)
		}

		simValues := []float64{}
		jaccValues := []float64{}

		for i := 0; i < numVectors; i++ {
			for j := i + 1; j < numVectors; j++ {
				simValues = append(simValues, similarity(vectors[i], vectors[j]))
				jaccValues = append(jaccValues, jaccard(vectors[i], vectors[j]))
			}
		}

		// Compute statistics
		simMean, simStd := computeStats(simValues)
		jaccMean, jaccStd := computeStats(jaccValues)

		fmt.Printf("Normalized Similarity: mean=%.4f, std=%.4f\n", simMean, simStd)
		fmt.Printf("Jaccard Similarity:    mean=%.4f, std=%.4f\n", jaccMean, jaccStd)

		fmt.Println("\nSimilarity Distribution (histogram):")
		bins := 10
		hist := make([]int, bins)
		for _, val := range simValues {
			binIdx := int(val * float64(bins))
			if binIdx >= bins {
				binIdx = bins - 1
			}
			hist[binIdx]++
		}

		for i, count := range hist {
			binStart := float64(i) / float64(bins)
			binEnd := float64(i+1) / float64(bins)
			bar := ""
			for j := 0; j < count/10; j++ {
				bar += "█"
			}
			fmt.Printf("[%.2f-%.2f): %s %d\n", binStart, binEnd, bar, count)
		}
		fmt.Println()
	}

	fmt.Println("=== Part 3: What happens for larger N? ===")
	fmt.Println("As N increases:")
	fmt.Println("1. Mean similarity approaches 0.5 (for random vectors with p=0.5)")
	fmt.Println("2. Standard deviation decreases (~ 1/√N by Central Limit Theorem)")
	fmt.Println("3. Distribution becomes MORE Gaussian (CLT)")
	fmt.Println("4. Reason: Similarity is average of many independent random variables")
	fmt.Println()

	N := 2000
	w := 5

	fmt.Printf("=== Part 4: Sparse Vectors ===\n")
	fmt.Printf("N = %d, w = %d\n", N, w)

	numPossible := binomial(N, w)
	fmt.Printf("Number of possible vectors: C(%d,%d) = %.2e\n", N, w, numPossible)
	fmt.Printf("In exact form: %d! / (%d! × %d!)\n", N, w, N-w)
	fmt.Println()

	fmt.Println("=== Part 5: Capacity of Sparse Binary Vectors ===")
	fmt.Println("Capacity can be defined as:")
	fmt.Println()
	fmt.Println("Information-theoretic capacity:")
	capacity := math.Log2(numPossible)
	fmt.Printf("  C = log₂(C(N,w)) = log₂(C(%d,%d)) ≈ %.2f bits\n", N, w, capacity)
	fmt.Println()
	fmt.Println("Pattern capacity (for associative memory):")
	fmt.Println("  If vectors are stored in a neural network with N neurons,")
	fmt.Printf("  and must be distinguishable, capacity ≈ N/(w×log(N/w))\n")
	fmt.Printf("  For our case: ≈ %d/(5×log(400)) ≈ %.1f patterns\n", N, float64(N)/(float64(w)*math.Log(float64(N)/float64(w))))
	fmt.Println()
	fmt.Println("Sparsity as capacity constraint:")
	sparsity := float64(w) / float64(N)
	fmt.Printf("  Sparsity: w/N = %d/%d = %.4f (%.2f%%)\n", w, N, sparsity, sparsity*100)
	fmt.Println("  Low sparsity → high capacity for distinguishing patterns")
	fmt.Println("  Each vector has w 'active features' out of N possible")
	fmt.Println()

	fmt.Println("Example sparse vectors:")
	for i := 0; i < 3; i++ {
		vec := generateSparseBinaryVector(N, w)
		positions := []int{}
		for j, v := range vec {
			if v == 1 {
				positions = append(positions, j)
			}
		}
		sort.Ints(positions)
		fmt.Printf("  Vector %d: ones at positions %v\n", i+1, positions)
	}
}
