package team.ae.algorithms.triemap.dto;

/**
 * Response DTO for semantic search.
 * <p>
 * It contains both the original item fields and the similarity score,
 * so that the client can see how "good" each match is.
 */
public record SearchResultDto(
        String id,
        String text,
        int clusterId,
        double similarity
) {

}