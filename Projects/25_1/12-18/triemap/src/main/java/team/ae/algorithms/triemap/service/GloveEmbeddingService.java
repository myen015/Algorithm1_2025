package team.ae.algorithms.triemap.service;

import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Primary;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import smile.nlp.embedding.GloVe;
import smile.nlp.embedding.Word2Vec;
import team.ae.algorithms.triemap.util.TextVectorizer;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Locale;

/**
 * Service for embedding text into dense numeric vectors using a pre-trained GloVe model.
 * This implementation leverages the SMILE library's Word2Vec functionality as a base.
 * The service provides text embeddings that can be used for various NLP tasks.
 */
@Slf4j
@Service
@Qualifier("gloveEmbeddingService")
@Primary
public class GloveEmbeddingService implements EmbeddingService {

    /**
     * Represents a pre-trained Word2Vec type model capable of generating dense vector
     * embeddings for individual words. This model is used as the underlying
     * implementation for converting text into numerical representations in the
     * GloveEmbeddingService.
     * <p>
     * Note: The model must be successfully loaded before it can be used.
     * An exception is thrown if any embedding operations are attempted prior
     * to the model's initialization.
     */
    private Word2Vec model;

    /**
     * Initializes the GloVe embedding model by loading it from a pre-defined file
     * located in the application's classpath: "static/glove.6B.300d.txt".
     * The method is automatically invoked after the Bean's creation due to the
     * {@code @PostConstruct} annotation.
     * <p>
     * @throws IllegalStateException if an I/O error occurs while loading the GloVe model
     */
    @PostConstruct
    public void init() {
        try {
            log.info("[GloveEmbeddingService] Loading GloVe model...");
            // The file should be located at: resources/static/glove.6B.300d.txt
            ClassPathResource resource = new ClassPathResource("static/glove.6B.300d.txt");

            File fileOnDisk = resource.getFile();
            this.model = GloVe.of(fileOnDisk.toPath());

            log.info("[GloveEmbeddingService] GloVe model loaded. " +
                    "dimension = {}", model.dimension());
        } catch (IOException exception) {
            throw new IllegalStateException("Failed to load GloVe model from classpath: static/glove.6B.300d.txt", exception);
        }
    }

    @Override
    public double[] embed(String text) {
        if (text == null || text.isBlank()) {
            return null;
        }
        if (model == null) {
            throw new IllegalStateException("GloVe/Word2Vec model is not loaded yet");
        }

        String[] tokens = text
                .toLowerCase(Locale.ROOT)
                .split("\\s+");

        double[] sum = null;
        int count = 0;

        for (String token : tokens) {
            // SMILE Word2Vec: apply(word) -> float[] or null
            float[] vector = model.apply(token);
            if (vector == null) {
                continue; // token isn't found in vocabulary
            }

            if (sum == null) {
                sum = new double[vector.length];
            }
            for (int i = 0; i < vector.length; i++) {
                sum[i] += vector[i];
            }
            count++;
        }

        if (count == 0) {
            return null;
        }

        int finalCount = count;
        double[] averaged = Arrays.stream(sum)
                .map(v -> v / finalCount)
                .toArray();

        TextVectorizer.l2Normalize(averaged);
        return averaged;
    }

}
