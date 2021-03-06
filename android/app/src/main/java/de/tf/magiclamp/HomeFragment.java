package de.tf.magiclamp;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.SeekBar;

import java.util.Map;

import butterknife.Bind;
import butterknife.ButterKnife;
import de.tf.magiclamp.model.LampConfig;
import retrofit.Callback;
import retrofit.RestAdapter;
import retrofit.RetrofitError;
import retrofit.client.Response;


/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link HomeFragment.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link HomeFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class HomeFragment extends Fragment {

    String TAG = "HomeFragment";
    public static LampConfig lampConfig;

    private Map generatorConfig;

    public static MagicLampService service;

    private static int MAX_BRIGHTNESS = 255;

    @Bind(R.id.nextButton)
    ImageButton nextButton;

    @Bind(R.id.powerButton)
    ImageButton powerButton;

    @Bind(R.id.brightnessBar)
    SeekBar brightnessBar;

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment HomeFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static HomeFragment newInstance() {
        HomeFragment fragment = new HomeFragment();
        Bundle args = new Bundle();
        fragment.setArguments(args);
        return fragment;
    }

    public HomeFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        RestAdapter restAdapter = new RestAdapter.Builder()
                .setEndpoint(Constants.ML_URL)
                .build();

        service = restAdapter.create(MagicLampService.class);
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nextGenerator();
            }
        });

        powerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                switchPower();
            }
        });

        final SeekBar brightnessBar = this.brightnessBar;
        service.getConfig(new Callback<LampConfig>() {

            @Override
            public void success(LampConfig lampConfig, Response response) {
                HomeFragment.lampConfig = lampConfig;
                brightnessBar.setProgress(lampConfig.getBrightness());
            }

            @Override
            public void failure(RetrofitError error) {
                Log.d(TAG, "getConfig() failed " + error);
            }
        });
        service.getGeneratorConfigList(new Callback<Map>() {
            @Override
            public void success(Map map, Response response) {
                generatorConfig = map;
            }

            @Override
            public void failure(RetrofitError error) {

            }
        });

        brightnessBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                if (lampConfig == null) {
                    return;
                }
                Log.d(TAG, "setting brightness to " + progress);
                LampConfig config = lampConfig;
                config.setBrightness(progress);

                service.setConfig(config, new Callback<LampConfig>() {

                    @Override
                    public void success(LampConfig aBoolean, Response response) {
                        Log.d(TAG, "setConfig() called " + lampConfig);
                    }

                    @Override
                    public void failure(RetrofitError error) {
                        Log.e(TAG, "setConfig() failed " + error);
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

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View result = inflater.inflate(R.layout.fragment_home, container, false);
        ButterKnife.bind(this, result);

        return result;
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }


    public void nextGenerator() {
        int generatorCount = generatorConfig.size();
        int newGeneratorIndex = lampConfig.getGeneratorIndex() + 1;
        if (newGeneratorIndex>=generatorCount) {
            newGeneratorIndex = 0;
        }

        this.lampConfig.setGeneratorIndex(newGeneratorIndex);

        service.setConfig(this.lampConfig, new Callback<LampConfig>() {
            @Override
            public void success(LampConfig lampConfig, Response response) {
                Log.d(TAG, "next() called");
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e(TAG, "next() failed", error);
            }
        });
    }

    public void switchPower() {
        if (lampConfig==null) {
            return;
        }

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


}
