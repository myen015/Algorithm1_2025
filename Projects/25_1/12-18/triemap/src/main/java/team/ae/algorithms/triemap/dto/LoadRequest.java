package team.ae.algorithms.triemap.dto;

import java.util.List;

/**
 * DTO used for JSON loading of items and cluster count.
 * Example JSON structure:
 * {
 * "kClusters": 4,
 * "texts": ["some text", "another text", ...]
 * }
 */
public record LoadRequest(int kClusters, List<String> texts) {

}
