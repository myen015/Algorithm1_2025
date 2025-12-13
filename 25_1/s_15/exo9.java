public class exo9 {

    /*
      Problem 1:
      Count number of finite functions:
      - {0,1}^n -> {0,1}
      - {0,1}^n -> {-1,0,1}
      - {0,1}^n -> {0,1}^m

      Problem 2:
     AND, OR, NOT using NAND

      Problem 3:
      idea why any Boolean function is computable
    */

    //Problem 1
    static void problem1(int n, int m) {
        int inputs = 1 << n;
        double f01 = Math.pow(2, inputs);
        double f3 = Math.pow(3, inputs);
        double f01m = Math.pow(2, m * inputs);
        System.out.println("Problem 1:");
        System.out.println("Functions {0,1}^" + n + " -> {0,1}: " + (long) f01);
        System.out.println("Functions {0,1}^" + n + " -> {-1,0,1}: " + (long) f3);
        System.out.println("Functions {0,1}^" + n + " -> {0,1}^" + m + ": " + (long) f01m);
        System.out.println();
    }

    //Problem 2
    static int NAND(int a, int b) {
        return (a == 1 && b == 1) ? 0 : 1;}
    static int NOT(int a) {
        return NAND(a, a);}
    static int AND(int a, int b) {
        return NOT(NAND(a, b));
    }
    static int OR(int a, int b) {
        return NAND(NOT(a), NOT(b));
    }
    static void problem2() {
        System.out.println("Problem 2:");
        for (int a = 0; a <= 1; a++) {
            for (int b = 0; b <= 1; b++) {
                System.out.println(
                    "A=" + a + " B=" + b +
                    " AND=" + AND(a,b) +
                    " OR=" + OR(a,b) +
                    " NOT(A)=" + NOT(a));
            }
        }
        System.out.println();
    }

    //Problem 3
    static void problem3(int n) {
        int inputs = 1 << n;
        long functions = (long) Math.pow(2, inputs);
        System.out.println("Problem 3:");
        System.out.println("Any Boolean function {0,1}^" + n + "-> {0,1}");
        System.out.println("Total possible functions: " + functions);
        System.out.println("Each function can be built using delta_x circuits");
        System.out.println("Circuit size: O(n * 2^n)");
        System.out.println();
    }

    public static void main(String[] args) {
        int n = 3;
        int m = 2;
        problem1(n, m);
        problem2();
        problem3(n);
    }
}
