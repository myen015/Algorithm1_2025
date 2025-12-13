package team.ae.algorithms.triemap.service;

import jakarta.annotation.PostConstruct;
import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.nd4j.common.io.ClassPathResource;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import team.ae.algorithms.triemap.util.TextVectorizer;

import java.io.File;
import java.util.Arrays;
import java.util.Locale;

/**
 * Provides Word2Vec embeddings via Deeplearning4j.
 * Model file is expected at: src/main/resources/static/GoogleNews-vectors-negative300.bin
 */
@Service
@Qualifier("word2vecEmbeddingService")
public class Word2VecEmbeddingService implements EmbeddingService {

    private Word2Vec model;

    @PostConstruct
    public void init() {
        try {
            ClassPathResource resource = new ClassPathResource("static/GoogleNews-vectors-negative300.bin");

            File file = resource.getFile();
            this.model = WordVectorSerializer.readWord2VecModel(file);

            System.out.println("[Word2VecEmbeddingService] Model loaded. " +
                    "Vector size = " + model.getLayerSize() +
                    ", vocab size = " + model.getVocab().numWords());

        } catch (Exception e) {
            throw new IllegalStateException("Failed to load Word2Vec model from classpath: static/GoogleNews-vectors-negative300.bin", e);
        }
    }

    @Override
    public double[] embed(String text) {
        if (text == null || text.isBlank()) {
            return null;
        }
        if (model == null) {
            throw new IllegalStateException("Word2Vec model is not loaded yet");
        }

        String[] tokens = text
                .toLowerCase(Locale.ROOT)
                .split("\\s+");

        int size = model.getLayerSize();
        double[] vectorSum = new double[size];
        int count = 0;

        for (String token : tokens) {
            if (model.hasWord(token)) {
                INDArray wordVec = model.getWordVectorMatrix(token);
                for (int i = 0; i < size; i++) {
                    vectorSum[i] += wordVec.getDouble(i);
                }
                count++;
            }
        }

        if (count == 0) {
            return null;
        }

        int finalCount = count;
        double[] averaged = Arrays.stream(vectorSum)
                .map(v -> v / finalCount)
                .toArray();


        TextVectorizer.l2Normalize(averaged);
        return averaged;
    }

}

