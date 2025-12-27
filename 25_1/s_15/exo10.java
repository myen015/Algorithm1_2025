public class exo10 {

    static double log2(double x) {
        return Math.log(x)/Math.log(2.0);
    }

    static double entropyBinary(double p) {
        double q =1.0-p;
        double h = 0.0;
        if (p>0) h+=-p*log2(p);
        if (q>0) h+=-q*log2(q);
        return h;
    }

    static double surprise(double prob) {
        return -log2(prob);
    }

    static void problem1() {
        System.out.println("Problem 1:");

        System.out.println("1) find max, linear search, shortest path in unweighted graph, matrix multiplication");
        System.out.println("   -> Class: P");

        System.out.println("2) sorting, Dijkstra(non-negative), BFS, DFS, merge sort, quicksort");
        System.out.println("   -> Class: P");

        System.out.println("3) sudoku");
        System.out.println("   -> Class: NP-complete (decision version), and also NP");

        System.out.println("4) 3-coloring of graph, scheduling with conflicts");
        System.out.println("   -> Class: NP-complete (and also NP)");

        System.out.println("5) TSP, Hamiltonian Cycle, Clique");
        System.out.println("   -> Class: NP-complete (decision versions), and also NP");

        System.out.println("6) Cryptography, factoring large integers");
        System.out.println("   -> Class: NP (not known to be in P; not known NP-complete).");
        System.out.println("      Factoring is also in coNP (but that's extra detail).");

        System.out.println("7) Halting Problem, Busy Beaver");
        System.out.println("   -> Class: Undecidable (not in P/NP). Often described as beyond NP-hard.\n");
    }

    //Problem 2
    static void problem2() {
        System.out.println("Problem 2:");

        //Given:
        //prevalence = 0.1% = 0.001
        //sensitivity = P(+ | disease) = 0.99
        //specificity = P(- | no disease) = 0.99  => false positive rate = 0.01
        double prevalence = 0.001;
        double sensitivity = 0.99;
        double specificity = 0.99;
        double falsePositive = 1.0 - specificity;

        double numerator = sensitivity * prevalence;
        double denominator = numerator + falsePositive * (1.0 - prevalence);
        double posterior = numerator / denominator;

        System.out.printf("P(Disease) = %.6f%n", prevalence);
        System.out.printf("Sensitivity P(+|D) = %.2f%n", sensitivity);
        System.out.printf("Specificity P(-|~D) = %.2f -> False positive P(+|~D)=%.2f%n",
                specificity, falsePositive);

        System.out.println("\nBayes:");
        System.out.println("P(D|+) = P(+|D)P(D)/(P(+|D)P(D)+P(+|~D)P(~D))");

        System.out.printf("P(D|+)=%.6f/%.6f=%.6f=%.2f%%%n%n",
                numerator, denominator, posterior, posterior * 100.0);

        System.out.println("Why about 9%?");
        System.out.println("- The disease is very rare (0.1%).");
        System.out.println("- Even with 99% specificity, false positives among healthy people dominate.\n");
    }


    static void problem3() {
        System.out.println("Problem 3: ");

        double pA = 0.50;
        double pB = 0.99;
        double pC = 0.01;

        double hA = entropyBinary(pA);
        double hB = entropyBinary(pB);
        double hC = entropyBinary(pC);

        System.out.printf("Coin A: P(H)=%.2f -> H(X)=%.6f bits%n", pA, hA);
        System.out.printf("Coin B: P(H)=%.2f -> H(X)=%.6f bits%n", pB, hB);
        System.out.printf("Coin C: P(H)=%.2f -> H(X)=%.6f bits%n%n", pC, hC);

        System.out.println("Surprise when HEADS happens: I(H) = -log2(P(H))");
        System.out.printf("Coin A: I(H)=%.6f bits (medium)%n", surprise(pA));
        System.out.printf("Coin B: I(H)=%.6f bits (tiny)%n", surprise(pB));
        System.out.printf("Coin C: I(H)=%.6f bits (HUGE)%n%n", surprise(pC));

        System.out.println("Explanation:");
        System.out.println("- Entropy is the average number of bits needed to describe outcomes.");
        System.out.println("- Fair coin (50/50) is maximally uncertain -> ~1 bit.");
        System.out.println("- Very biased coin (99/1) is predictable -> very low entropy (~0.08 bits).");
        System.out.println("- Note: P(H)=0.99 and P(H)=0.01 have the same entropy (symmetry).");
    }

    public static void main(String[] args) {
        problem1();
        problem2();
        problem3();
    }
}
