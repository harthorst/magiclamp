package de.tf.magiclamp.model;

/**
 * Created by tf on 8/18/15.
 */
public class LampConfig {
    private int brightness;

    private boolean active;

    private int generatorIndex;

    public int getGeneratorIndex() {
        return generatorIndex;
    }

    public void setGeneratorIndex(int generatorIndex) {
        this.generatorIndex = generatorIndex;
    }

    public boolean getActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public int getBrightness() {
        return brightness;
    }

    public void setBrightness(int brightness) {
        this.brightness = brightness;
    }
}
