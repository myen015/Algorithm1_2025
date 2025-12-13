package team.ae.algorithms.triemap.dto;

public record KMeansResult(
        int[] labels,
        double[][] centroids
) {}
