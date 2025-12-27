import java.util.*;

public class exo8 {

    /*
      Problem 1:
        - reverse graph
        - SCC(Kosaraju)
        - SCC graph is DAG
      Problem 2:
        - Euler tour(directed)
        - inDegree == outDegree
        - Hierholzer
      Problem 3:
        - Topological order(Kahn)
    */

    //Directed graph
    static class DiGraph {
        int n;
        List<Integer>[] adj;

        @SuppressWarnings("unchecked")
        DiGraph(int n) {
            this.n = n;
            adj = new ArrayList[n];
            for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        }

        void addEdge(int u, int v) {
            adj[u].add(v);
        }

        DiGraph reverse() {
            DiGraph r = new DiGraph(n);
            for (int u = 0; u < n; u++) {
                for (int v : adj[u]) r.addEdge(v, u);
            }
            return r;
        }
    }

    //Problem 1: SCC
    static class SCCResult {
        int compCount;
        int[] compId;
        List<List<Integer>> comps;
        DiGraph dag;
    }

    static SCCResult sccKosaraju(DiGraph g) {
        int n = g.n;
        boolean[] used = new boolean[n];
        List<Integer> order = new ArrayList<>();

        for (int i = 0; i < n; i++)
            if (!used[i]) dfs1(g, i, used, order);

        DiGraph gr = g.reverse();
        Arrays.fill(used, false);

        int[] compId = new int[n];
        Arrays.fill(compId, -1);
        Collections.reverse(order);

        List<List<Integer>> comps = new ArrayList<>();
        int cid = 0;

        for (int v : order) {
            if (!used[v]) {
                List<Integer> cur = new ArrayList<>();
                dfs2(gr, v, used, compId, cid, cur);
                comps.add(cur);
                cid++;
            }
        }

        DiGraph dag = new DiGraph(cid);
        Set<Long> seen = new HashSet<>();
        for (int u = 0; u < n; u++) {
            for (int v : g.adj[u]) {
                int cu = compId[u], cv = compId[v];
                if (cu != cv) {
                    long key = (((long) cu)<<32) ^ (cv & 0xffffffffL);
                    if (seen.add(key)) dag.addEdge(cu, cv);
                }
            }
        }

        SCCResult res = new SCCResult();
        res.compCount = cid;
        res.compId = compId;
        res.comps = comps;
        res.dag = dag;
        return res;
    }

    static void dfs1(DiGraph g, int v, boolean[] used, List<Integer> order) {
        used[v] = true;
        for (int to : g.adj[v])
            if (!used[to]) dfs1(g, to, used, order);
        order.add(v);
    }

    static void dfs2(DiGraph g, int v, boolean[] used, int[] compId, int cid, List<Integer> cur) {
        used[v] = true;
        compId[v] = cid;
        cur.add(v);
        for (int to : g.adj[v])
            if (!used[to]) dfs2(g, to, used, compId, cid, cur);
    }

    //roblem 2: Euler tour
    static List<Integer> eulerTour(DiGraph g, int start) {
        int n = g.n;
        int[] in = new int[n];
        int[] out = new int[n];

        for (int u = 0; u < n; u++) {
            out[u] = g.adj[u].size();
            for (int v : g.adj[u]) in[v]++;
        }

        for (int i = 0; i < n; i++)
            if (in[i] != out[i]) return null;

        List<ArrayDeque<Integer>> work = new ArrayList<>(n);
        for (int i = 0; i < n; i++)
            work.add(new ArrayDeque<>(g.adj[i]));

        ArrayDeque<Integer> st = new ArrayDeque<>();
        List<Integer> ans = new ArrayList<>();
        st.push(start);

        while (!st.isEmpty()) {
            int v = st.peek();
            if (!work.get(v).isEmpty()) {
                int to = work.get(v).pollFirst();
                st.push(to);
            } else {
                ans.add(st.pop());
            }
        }

        Collections.reverse(ans);
        return ans;
    }

    //Problem 3: Topological order
    static List<String> topoOrder(Map<String, List<String>> g, String preferFirst) {
        LinkedHashSet<String> V = new LinkedHashSet<>();
        for (String u : g.keySet()) {
            V.add(u);
            V.addAll(g.get(u));
        }

        Map<String, Integer> indeg = new HashMap<>();
        for (String v : V) indeg.put(v, 0);
        for (String u : g.keySet())
            for (String v : g.get(u)) indeg.put(v, indeg.get(v) + 1);

        ArrayDeque<String> q = new ArrayDeque<>();
        List<String> zeros = new ArrayList<>();
        for (String v : V) if (indeg.get(v) == 0) zeros.add(v);

        if (zeros.remove(preferFirst)) q.add(preferFirst);
        for (String z : zeros) q.add(z);

        List<String> order = new ArrayList<>();
        while (!q.isEmpty()) {
            String u = q.pollFirst();
            order.add(u);
            for (String v : g.getOrDefault(u, Collections.emptyList())) {
                indeg.put(v, indeg.get(v) - 1);
                if (indeg.get(v) == 0) q.addLast(v);
            }
        }

        if (order.size() != V.size()) return null;
        return order;
    }

    static void printIntGraph(DiGraph g, String title) {
        System.out.println(title);
        for (int u = 0; u < g.n; u++)
            System.out.println("  " + u + " -> " + g.adj[u]);
        System.out.println();
    }

    static void printDag(DiGraph dag, String title) {
        System.out.println(title);
        for (int c = 0; c < dag.n; c++) {
            List<String> outs = new ArrayList<>();
            for (int to : dag.adj[c]) outs.add("C" + to);
            System.out.println("  C" + c + " -> " + outs);
        }
        System.out.println();
    }

    public static void main(String[] args) {

        DiGraph g1 = new DiGraph(5);
        g1.addEdge(0, 1);
        g1.addEdge(1, 2);
        g1.addEdge(2, 0);
        g1.addEdge(2, 3);
        g1.addEdge(3, 4);
        g1.addEdge(4, 3);

        printIntGraph(g1, "Problem 1: G");
        printIntGraph(g1.reverse(), "Problem 1: reverse(G)");

        SCCResult scc = sccKosaraju(g1);
        System.out.println("Problem 1: SCCs");
        for (int i = 0; i < scc.comps.size(); i++)
            System.out.println("  C" + i + " = " + scc.comps.get(i));
        System.out.println();
        printDag(scc.dag, "Problem 1: SCC graph");

        DiGraph eg = new DiGraph(3);
        eg.addEdge(0, 1);
        eg.addEdge(1, 2);
        eg.addEdge(2, 0);
        eg.addEdge(0, 2);
        eg.addEdge(2, 1);
        eg.addEdge(1, 0);

        printIntGraph(eg, "Problem 2: Euler graph");
        System.out.println("Problem 2: Euler tour = " + eulerTour(eg, 0));
        System.out.println();

        Map<String, List<String>> courses = new LinkedHashMap<>();
        courses.put("A", Arrays.asList("B", "C"));
        courses.put("B", Arrays.asList("C", "D"));
        courses.put("C", Arrays.asList("E"));
        courses.put("D", Arrays.asList("E", "F"));
        courses.put("G", Arrays.asList("F", "E"));

        System.out.println("Problem 3: topo (prefer A) = "+ topoOrder(courses, "A"));
        System.out.println("Problem 3: topo (prefer G) = "+ topoOrder(courses, "G"));
    }
}
