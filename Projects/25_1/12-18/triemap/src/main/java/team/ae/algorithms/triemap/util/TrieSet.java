package team.ae.algorithms.triemap.util;

import java.util.ArrayList;
import java.util.List;

public class TrieSet {
    // every Node has 26 size empty array filled with 'null' nodes, every time a letter is inserted we

    private static class Node {
        Node[] next = new Node[26];
        boolean end;
    }

    private final Node root = new Node();

    private static int idx(char character) {
        if (character >= 'a' && character <= 'z') return character - 'a';
        throw new IllegalArgumentException("only a..z");
    }

    private static String norm(String s) {
        return s == null ? "" : s.trim().toLowerCase();
    }

    public void insert(String word) {
        String normalizedWord = norm(word);
        if (normalizedWord.isEmpty()) return;
        Node cur = root;
        for (int i = 0; i < normalizedWord.length(); i++) {
            int k = idx(normalizedWord.charAt(i));
            if (cur.next[k] == null) cur.next[k] = new Node();
            cur = cur.next[k];
        }
        cur.end = true;
    }

    public boolean contains(String word) {
        String normalizedWord = norm(word);
        if (normalizedWord.isEmpty()) return false;
        Node current = root;
        for (int i = 0; i < normalizedWord.length(); i++) {
            int k = idx(normalizedWord.charAt(i));
            if (current.next[k] == null) return false;
            current = current.next[k];
        }
        return current.end;
    }

    public List<String> suggest(String prefix, int limit) {
        String normalizedPrefix = norm(prefix);
        Node current = root;
        for (int i = 0; i < normalizedPrefix.length(); i++) {
            int k = idx(normalizedPrefix.charAt(i));
            if (current.next[k] == null) return List.of();
            current = current.next[k];
        }
        List<String> output = new ArrayList<>();
        dfs(current, new StringBuilder(normalizedPrefix), limit <= 0 ? Integer.MAX_VALUE : limit, output);
        return output;
    }

    private void dfs(Node node, StringBuilder path, int limit, List<String> output) {
        if (output.size() >= limit) return;
        if (node.end) {
            output.add(path.toString());
            if (output.size() >= limit) return;
        }
        for (int i = 0; i < 26; i++) {
            if (node.next[i] == null) continue;
            path.append((char) ('a' + i));
            dfs(node.next[i], path, limit, output);
            path.setLength(path.length() - 1);
            if (output.size() >= limit) return;
        }
    }
}