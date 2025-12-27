package team.ae.algorithms.triemap.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;

public record Item(String id,
                   String text,
                   @JsonIgnore double[] vector,
                   int clusterId) {

    //redundant memory usage: consider changing record to class and refactor for larger items collection
    public Item withCluster(int newClusterId) {
        return new Item(id, text, vector, newClusterId);
    }

}
