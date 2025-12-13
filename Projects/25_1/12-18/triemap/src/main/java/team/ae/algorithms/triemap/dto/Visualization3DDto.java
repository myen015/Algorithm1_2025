package team.ae.algorithms.triemap.dto;

import java.util.List;

public record Visualization3DDto(
        List<Centroid3D> centroids,
        List<Point3D> points
) {}
