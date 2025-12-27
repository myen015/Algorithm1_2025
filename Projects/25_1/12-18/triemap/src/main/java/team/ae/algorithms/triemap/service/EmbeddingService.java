package team.ae.algorithms.triemap.service;

/**
 * Abstraction for converting text into numeric embeddings.
 * Today we use a simple character-based embedding,
 * but later this can be replaced by a real Word2Vec / GloVe model.
 */
public interface EmbeddingService {

    /**
     * Converts given text into a dense numeric vector.
     */
    double[] embed(String text);
}