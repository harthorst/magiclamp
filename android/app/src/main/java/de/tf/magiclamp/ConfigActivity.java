package de.tf.magiclamp;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.SeekBar;

import java.util.HashMap;
import java.util.Map;

import retrofit.Callback;
import retrofit.RestAdapter;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class ConfigActivity extends Activity {

    MagicLampService service;
    Map config = new HashMap();
    String TAG = "ConfigActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_config);

        RestAdapter restAdapter = new RestAdapter.Builder()
                .setEndpoint(Constants.ML_URL)
                .build();

        service = restAdapter.create(MagicLampService.class);

        final Map config = this.config;

        final SeekBar seekBarRed = (SeekBar)findViewById(R.id.seekBarRed);
        final SeekBar seekBarGreen = (SeekBar)findViewById(R.id.seekBarGreen);
        final SeekBar seekBarBlue = (SeekBar)findViewById(R.id.seekBarBlue);

        // TODO: tf
        service.getGeneratorConfig(2, new Callback<Map>() {

            @Override
            public void success(Map config, Response response) {
                Log.d(TAG, "got config " + config);
                config.putAll(config);
                Map<String, Double> color = (Map<String, Double>) config.get("color");
                seekBarRed.setProgress((int) (double) Double.valueOf(color.get("r") * 100 / 255));
                seekBarGreen.setProgress((int) (double) Double.valueOf(color.get("g") * 100 / 255));
                seekBarBlue.setProgress((int) (double) Double.valueOf(color.get("b") * 100 / 255));

                seekBarRed.setOnSeekBarChangeListener(new Listener("r", service, config, 1));
                seekBarGreen.setOnSeekBarChangeListener(new Listener("g", service, config, 1));
                seekBarBlue.setOnSeekBarChangeListener(new Listener("b", service, config, 1));
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e(TAG, "error fetching config " + error);
            }
        });
    }

    private class Listener implements SeekBar.OnSeekBarChangeListener {
        String key;
        MagicLampService service;
        int id;
        Map config;

        public Listener(String key, MagicLampService service, Map config, int id) {
            this.key = key;
            this.service = service;
            this.config = config;
            this.id = id;
        }

        @Override
        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            Map<String, Double> color = (Map<String, Double>) config.get("color");
            Double colorVal = Double.valueOf(progress * 255 / 100);
            color.put(this.key, colorVal);

            service.setGeneratorConfig(id, config, new Callback<Map>() {

                @Override
                public void success(Map map, Response response) {
                    Log.d(TAG,"success");
                }

                @Override
                public void failure(RetrofitError error) {
                    Log.e(TAG, "failed " + error);
                }
            });
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {

        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {

        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_config, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
