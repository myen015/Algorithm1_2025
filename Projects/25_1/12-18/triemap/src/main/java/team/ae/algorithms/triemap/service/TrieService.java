package team.ae.algorithms.triemap.service;

import org.springframework.stereotype.Service;
import team.ae.algorithms.triemap.util.TrieMap;
import team.ae.algorithms.triemap.util.TrieSet;

import java.util.Collection;
import java.util.List;

@Service
public class TrieService {
  private final TrieSet set = new TrieSet();
  private final TrieMap map = new TrieMap();

  // ===== TrieSet API =====
  public void setInsert(String word) { set.insert(word); }
  public boolean setContains(String word) { return set.contains(word); }
  public List<String> setSuggest(String prefix, int limit) { return set.suggest(prefix, limit); }

  // ===== TrieMap API =====
  public void mapPut(String key, String value) { map.put(key, value); }
  public String mapGet(String key) { return map.get(key); }
  public boolean mapContains(String key) { return map.containsKey(key); }
  public List<String> mapKeys(String prefix, int limit) { return map.keysWithPrefix(prefix, limit); }

  public void preloadSet(Collection<String> words) { if (words!=null) words.forEach(set::insert); }
  public void preloadMap(Collection<String> keys, String fixedValue) {
    if (keys!=null) keys.forEach(k -> map.put(k, fixedValue));
  }
}