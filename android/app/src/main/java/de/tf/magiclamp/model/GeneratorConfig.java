package de.tf.magiclamp.model;

/**
 * Created by tf on 9/1/15.
 */
public class GeneratorConfig {
    private String name;
    private String hash;
    private int generatorIndex;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getHash() {
        return hash;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }

    public int getGeneratorIndex() {
        return generatorIndex;
    }

    public void setGeneratorIndex(int generatorIndex) {
        this.generatorIndex = generatorIndex;
    }
}
