package team.ae.algorithms.triemap.util;

import java.util.ArrayList;
import java.util.List;

public class TrieMap {
    private static class Node {
        Node[] next = new Node[26];
        boolean end;
        String value;
    }
    private final Node root = new Node();

    private static int idx(char c) {
        if (c >= 'a' && c <= 'z') return c - 'a';
        throw new IllegalArgumentException("only a..z");
    }
    private static String norm(String s) {
        return s == null ? "" : s.trim().toLowerCase();
    }

    public void put(String key, String value) {
        String normalizedKey = norm(key); if (normalizedKey.isEmpty()) return;
        Node current = root;
        for (int i = 0; i< normalizedKey.length(); i++) {
            int j = idx(normalizedKey.charAt(i));
            if (current.next[j] == null) current.next[j] = new Node();
            current = current.next[j];
        }


        current.end = true;
        current.value = value;
    }

    public String get(String key) {
        String normalizedKey = norm(key); if (normalizedKey.isEmpty()) return null;
        Node current = root;
        for (int i = 0; i< normalizedKey.length(); i++) {
            int j = idx(normalizedKey.charAt(i));
            if (current.next[j] == null) return null;
            current = current.next[j];
        }
        return current.end ? current.value : null;
    }

    public boolean containsKey(String key) {
        String normalizedKey = norm(key); if (normalizedKey.isEmpty()) return false;
        Node current = root;
        for (int i = 0; i< normalizedKey.length(); i++) {
            int j = idx(normalizedKey.charAt(i));
            if (current.next[j] == null) return false;
            current = current.next[j];
        }
        return current.end;
    }

    public List<String> keysWithPrefix(String prefix, int limit) {
        String p = norm(prefix);
        Node cur = root;
        for (int i=0;i<p.length();i++) {
            int j = idx(p.charAt(i));
            if (cur.next[j] == null) return List.of();
            cur = cur.next[j];
        }
        List<String> out = new ArrayList<>();
        dfs(cur, new StringBuilder(p), limit<=0?Integer.MAX_VALUE:limit, out);
        return out;
    }

    private void dfs(Node n, StringBuilder path, int limit, List<String> out) {
        if (out.size() >= limit) return;
        if (n.end) {
            out.add(path.toString());
            if (out.size() >= limit) return;
        }
        for (int i=0;i<26;i++) {
            if (n.next[i] == null) continue;
            path.append((char)('a'+i));
            dfs(n.next[i], path, limit, out);
            path.setLength(path.length()-1);
            if (out.size() >= limit) return;
        }
    }
}
