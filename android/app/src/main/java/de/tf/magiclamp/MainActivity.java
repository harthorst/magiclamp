package de.tf.magiclamp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.SeekBar;

import de.tf.magiclamp.model.LampConfig;
import retrofit.Callback;
import retrofit.RestAdapter;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class MainActivity extends Activity {

    String TAG = "MainActivity";
    public static LampConfig lampConfig = new LampConfig();

    MagicLampService service;

    public void nextGenerator(View v) {
        service.next(new Callback<Boolean>() {

            @Override
            public void success(Boolean aBoolean, Response response) {
                Log.d(TAG, "next() called");
            }

            @Override
            public void failure(RetrofitError error) {
                Log.d(TAG, "next() failed");
            }
        });
    }

    public void switchPower(View v) {

        lampConfig.setActive(!lampConfig.getActive());

        service.setConfig(lampConfig, new Callback<LampConfig>() {

            @Override
            public void success(LampConfig aBoolean, Response response) {
                Log.d(TAG, "setConfig() called");
            }

            @Override
            public void failure(RetrofitError error) {
                Log.d(TAG, "setConfig() failed " + error);
            }
        });
    }

    public void configure(View v) {
        Intent i = new Intent(this, ConfigActivity.class);
        startActivity(i);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        RestAdapter restAdapter = new RestAdapter.Builder()
                .setEndpoint(Constants.ML_URL)
                .build();

        service = restAdapter.create(MagicLampService.class);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);

        final SeekBar brightnessBar = (SeekBar) findViewById(R.id.brightnessBar);
        service.getConfig(new Callback<LampConfig>() {

            @Override
            public void success(LampConfig lampConfig, Response response) {
                MainActivity.lampConfig = lampConfig;
                brightnessBar.setProgress(100 * lampConfig.getBrightness() / 255);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.d(TAG, "getConfig() failed " + error);
            }
        });

        brightnessBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                Log.d(TAG, "setting brightness to " + progress + "%");
                LampConfig config = lampConfig;
                config.setBrightness(255 * progress / 100);

                service.setConfig(config, new Callback<LampConfig>() {

                    @Override
                    public void success(LampConfig aBoolean, Response response) {
                        Log.d(TAG, "setConfig() called");
                    }

                    @Override
                    public void failure(RetrofitError error) {
                        Log.d(TAG, "setConfig() failed " + error);
                    }
                });
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

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
