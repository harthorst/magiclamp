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


public class RGBConfigFragment extends Fragment {

    static final String TAG = "RGBConfigFragment";
    static final String KEY_GENERATOR_INDEX = "generatorIndex";

    @Bind(R.id.seekBarRed)
    SeekBar seekBarRed;
    @Bind(R.id.seekBarGreen)
    SeekBar seekBarGreen;
    @Bind(R.id.seekBarBlue)
    SeekBar seekBarBlue;

    private Map generatorConfig;

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment RGBConfig.
     */
    public static RGBConfigFragment newInstance(Integer generatorIndex) {
        RGBConfigFragment fragment = new RGBConfigFragment();
        Bundle args = new Bundle();
        args.putInt(KEY_GENERATOR_INDEX, generatorIndex);
        fragment.setArguments(args);
        return fragment;
    }

    public RGBConfigFragment() {
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

        View result = inflater.inflate(R.layout.fragment_rgb_config, container, false);
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
                Map<String, Double> color = (Map<String, Double>)map.get("color");
                int red = color.get("r").intValue();
                int green = color.get("g").intValue();
                int blue = color.get("b").intValue();
                seekBarRed.setProgress(red);
                seekBarGreen.setProgress(green);
                seekBarBlue.setProgress(blue);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e(TAG, "setConfig() failed ", error);
            }
        });

        seekBarRed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
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

        seekBarGreen.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
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

        seekBarBlue.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
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
        Map<String, Double> color = (Map<String, Double>)generatorConfig.get("color");
        color.put("r", Double.valueOf(seekBarRed.getProgress()));
        color.put("g", Double.valueOf(seekBarGreen.getProgress()));
        color.put("b", Double.valueOf(seekBarBlue.getProgress()));

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
