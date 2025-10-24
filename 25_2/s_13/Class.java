import java.util.*;
public class Class {
    public static void main(String[] args) {
        Scanner css = new Scanner(System.in);
        int n = css.nextInt();
        int[] array = new int[n]; // n number

        for (int i = 1; i <= n; i++) {
            array[i- 1] = css.nextInt();
        } // here we used input datas, it will be any data unsorted

        System.out.println(Arrays.toString(array));
        // we will check and see before sorting:

        int i = 1;
        while (i < n){
            if(i == 0 || array[i-1] <= array[i]){
                i++;
                // this line checks that if comparing i with i + 1 position
                // and if it is right comparing it will be continued to find unsorted pivot
            }else{
                int save = array[i];
                array[i] = array[i-1];
                array[i-1] = save;
                i--;
                // in else case, we will change datas for position. like smaller will go back
                // and we will check it again.
            }
        }
        System.out.println(Arrays.toString(array));
        // here after sorting.
        // finally: O(n^2) speed.
        int[] array2 = {1, 5 ,3, 2, 4};
        Arrays.sort(array2);
        System.out.println(Arrays.toString(array2));
    }
}












