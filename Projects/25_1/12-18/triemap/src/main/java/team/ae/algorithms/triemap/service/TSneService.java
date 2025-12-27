package team.ae.algorithms.triemap.service;

import org.springframework.stereotype.Service;
import smile.manifold.TSNE;
import team.ae.algorithms.triemap.dto.Visualization2D;
import team.ae.algorithms.triemap.dto.Visualization3D;

import java.util.ArrayList;
import java.util.List;

/**
 * t-SNE dimensionality reduction for 2D and 3D visualization.
 */
@Service
public class TSneService {

    /**
     * Reduce high-dimensional vectors to 2D using t-SNE.
     *
     * @param highDim array of high-dimensional vectors [n x d]
     * @param clusterLabels optional cluster labels for each point
     * @return list of Visualization2D results
     */
    public List<Visualization2D> reduceTo2D(double[][] highDim, int[] clusterLabels) {
        if (highDim == null || highDim.length == 0) {
            return List.of();
        }

        // Run t-SNE; SMILE returns a TSNE record containing cost + coordinates
        TSNE tsneResult = TSNE.fit(highDim);
        double[][] lowDim = tsneResult.coordinates();

        List<Visualization2D> result = new ArrayList<>();
        for (int i = 0; i < lowDim.length; i++) {
            result.add(new Visualization2D(
                    i,
                    lowDim[i][0],
                    lowDim[i][1],
                    clusterLabels != null ? clusterLabels[i] : -1
            ));
        }
        return result;
    }

    /**
     * Reduce high-dimensional vectors to 3D using t-SNE.
     *
     * @param highDim array of high-dimensional vectors [n x d]
     * @param clusterLabels optional cluster labels for each point
     * @return list of Visualization3D results
     */
    public List<Visualization3D> reduceTo3D(double[][] highDim, int[] clusterLabels) {
        if (highDim == null || highDim.length == 0) {
            return List.of();
        }

        var options = new TSNE.Options(3, 20, 200, 12, 1000);
        TSNE tsneResult = TSNE.fit(highDim, options);
        double[][] lowDim = tsneResult.coordinates();

        List<Visualization3D> result = new ArrayList<>();
        for (int i = 0; i < lowDim.length; i++) {
            // If the model returned 2D coords, we fall back to 0 for z
            double x = lowDim[i].length > 0 ? lowDim[i][0] : 0.0;
            double y = lowDim[i].length > 1 ? lowDim[i][1] : 0.0;
            double z = lowDim[i].length > 2 ? lowDim[i][2] : 0.0;

            result.add(new Visualization3D(
                    i, x, y, z, clusterLabels != null ? clusterLabels[i] : -1
            ));
        }
        return result;
    }
}