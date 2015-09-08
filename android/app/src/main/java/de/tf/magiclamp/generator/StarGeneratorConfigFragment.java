package de.tf.magiclamp.generator;

import android.app.Activity;
import android.app.Fragment;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.SeekBar;

import java.util.Map;

import butterknife.Bind;
import butterknife.ButterKnife;
import de.tf.magiclamp.HomeFragment;
import de.tf.magiclamp.R;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;


public class StarGeneratorConfigFragment extends Fragment {

    static final String TAG = "StarGeneratorConfigFragment";
    static final String KEY_GENERATOR_INDEX = "generatorIndex";
    static final int MAX_RESPAWN_TIME = 5000;
    static final int MAX_STARS = 20;
    static final int MAX_STAR_SIZE = 10;

    @Bind(R.id.seekBarMaxStarSize)
    SeekBar seekBarMaxStarSize;
    @Bind(R.id.seekBarMaxRespawnTime)
    SeekBar seekBarMaxRespawnTime;
    @Bind(R.id.seekBarMaxStars)
    SeekBar seekBarMaxStars;

    private Map generatorConfig;

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment RGBConfig.
     */
    public static StarGeneratorConfigFragment newInstance(Integer generatorIndex) {
        StarGeneratorConfigFragment fragment = new StarGeneratorConfigFragment();
        Bundle args = new Bundle();
        args.putInt(KEY_GENERATOR_INDEX, generatorIndex);
        fragment.setArguments(args);
        return fragment;
    }

    public StarGeneratorConfigFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment

        View result = inflater.inflate(R.layout.fragment_star_generator_config, container, false);
        ButterKnife.bind(this, result);

        return result;
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        int generatorIndex = this.getArguments().getInt(KEY_GENERATOR_INDEX);

        HomeFragment.service.getGeneratorConfig(generatorIndex, new Callback<Map>() {
            @Override
            public void success(Map map, Response response) {
                generatorConfig = map;
                Map<String, Double> generatorConfig = (Map<String, Double>) map;
                int maxRespawnTime = generatorConfig.get("maxRespawnTime").intValue();
                int maxPointSize = generatorConfig.get("maxPointSize").intValue();
                int maxPoints = generatorConfig.get("maxPoints").intValue();
                seekBarMaxRespawnTime.setProgress(100 * maxRespawnTime / MAX_RESPAWN_TIME);
                seekBarMaxStarSize.setProgress(100 * maxPointSize / MAX_STAR_SIZE);
                seekBarMaxStars.setProgress(100 * maxPoints / MAX_STARS);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e(TAG, "setConfig() failed ", error);
            }
        });

        seekBarMaxRespawnTime.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                updateConfig();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        seekBarMaxStarSize.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                updateConfig();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        seekBarMaxStars.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                updateConfig();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

    }

    private void updateConfig() {
        generatorConfig.put("maxRespawnTime", (int) (MAX_RESPAWN_TIME * seekBarMaxRespawnTime.getProgress() / 100 ));
        generatorConfig.put("maxPointSize", (int) (MAX_STAR_SIZE * seekBarMaxStarSize.getProgress() / 100 ));
        generatorConfig.put("maxPoints", (int) (MAX_STARS * seekBarMaxStars.getProgress() / 100 ));

        int generatorIndex = this.getArguments().getInt(KEY_GENERATOR_INDEX);
        HomeFragment.service.setGeneratorConfig(generatorIndex, generatorConfig, new Callback<Map>() {
            @Override
            public void success(Map map, Response response) {
                Log.d(TAG, "setConfig() success " + generatorConfig);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e(TAG, "setConfig() error", error);
            }
        });
    }

    // TODO: Rename method, update argument and hook method into UI event
    public void onButtonPressed(Uri uri) {
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }
}
