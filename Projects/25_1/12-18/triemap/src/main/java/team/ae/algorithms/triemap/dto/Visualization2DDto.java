package team.ae.algorithms.triemap.dto;

import java.util.List;

public record Visualization2DDto(
        List<Centroid2D> centroids,
        List<Point2D> points
) {}
