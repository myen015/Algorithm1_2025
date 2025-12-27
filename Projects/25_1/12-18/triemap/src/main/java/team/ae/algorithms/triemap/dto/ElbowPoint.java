package team.ae.algorithms.triemap.dto;

/**
 * Holds the result of elbow analysis:
 * - k: number of clusters
 * - inertia: sum of squared distances of points to their assigned centroid(WSS)
 */
public record ElbowPoint(int k, double inertia) {}