package de.tf.magiclamp.model;

/**
 * Created by tf on 8/18/15.
 */
public class LampConfig {
    private int brightness;

    private boolean active;

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
