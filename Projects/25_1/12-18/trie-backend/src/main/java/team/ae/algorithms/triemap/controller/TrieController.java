package team.ae.algorithms.triemap.controller;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import team.ae.algorithms.triemap.service.TrieService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class TrieController {

  private final TrieService service;
  public TrieController(TrieService service) {
    this.service = service;

    service.preloadSet(List.of("apple","app","apply","apt","dog","door"));
    service.preloadMap(List.of("cat","car","cart"), "value");
  }

  // ===== TrieSet =====
  public record InsertReq(String word) {}

  @PostMapping("/trie-set/insert")
  @ResponseStatus(HttpStatus.NO_CONTENT)
  public void setInsert(@RequestBody InsertReq req) {
    if (req != null && req.word()!=null) service.setInsert(req.word());
  }

  @GetMapping("/trie-set/contains")
  public boolean setContains(@RequestParam("q") String q) {
    return service.setContains(q);
  }

  @GetMapping("/trie-set/suggest")
  public List<String> setSuggest(@RequestParam("q") String q,
                                 @RequestParam(value="k", defaultValue="10") int k) {
    return service.setSuggest(q, k);
  }

  // ===== TrieMap =====
  public record PutReq(String key, String value) {}
  public record GetResp(String key, String value) {}

  @PostMapping("/trie-map/put")
  @ResponseStatus(HttpStatus.NO_CONTENT)
  public void mapPut(@RequestBody PutReq req) {
    if (req != null && req.key()!=null) service.mapPut(req.key(), req.value());
  }

  @GetMapping("/trie-map/get")
  public GetResp mapGet(@RequestParam("key") String key) {
    return new GetResp(key, service.mapGet(key));
  }

  @GetMapping("/trie-map/contains")
  public Map<String, Boolean> mapContains(@RequestParam("key") String key) {
    return Map.of("ok", service.mapContains(key));
  }

  @GetMapping("/trie-map/keys")
  public List<String> mapKeys(@RequestParam("q") String q,
                              @RequestParam(value="k", defaultValue="10") int k) {
    return service.mapKeys(q, k);
  }
}