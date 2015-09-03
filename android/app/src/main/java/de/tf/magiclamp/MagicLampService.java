package de.tf.magiclamp;

import java.util.Map;

import de.tf.magiclamp.model.LampConfig;
import retrofit.http.Body;
import retrofit.http.GET;
import retrofit.Callback;
import retrofit.http.PUT;
import retrofit.http.Path;

/**
 * Created by tf on 8/18/15.
 */
public interface MagicLampService {
    @GET("/next")
    public void next(Callback<Boolean> callback);

    @PUT("/config")
    public void setConfig(@Body LampConfig config, Callback<LampConfig> callback);

    @GET("/config")
    public void getConfig(Callback<LampConfig> c);

    @GET("/generatorConfig")
    public void getGeneratorConfigList(Callback<Map> c);

    @GET("/generatorConfig/{id}")
    public void getGeneratorConfig(@Path("id") int id, Callback<Map> c);

    @PUT("/generatorConfig/{id}")
    public void setGeneratorConfig(@Path("id") int id, @Body Map config, Callback<Map> c);
}
