package de.tf.magiclamp.generator;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
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

/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link FloatingPointGeneratorConfig.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link FloatingPointGeneratorConfig#newInstance} factory method to
 * create an instance of this fragment.
 */
public class FloatingPointGeneratorConfigFragment extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    static final int MAX_SPEED = 20;
    static final int MAX_POINTS = 20;
    static final int MAX_TAIL_LENGTH = 10;

    static final String TAG = "FloatingPointGenConfigFrag";

    @Bind(R.id.seekBarMinSpeed)
    SeekBar seekBarMinSpeed;
    @Bind(R.id.seekBarMaxSpeed)
    SeekBar seekBarMaxSpeed;
    @Bind(R.id.seekBarMaxPoints)
    SeekBar seekBarMaxPoints;
    @Bind(R.id.seekBarTailLength)
    SeekBar seekBarTailLength;

    private Map generatorConfig;

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment FloatingPointGeneratorConfig.
     */
    // TODO: Rename and change types and number of parameters
    public static FloatingPointGeneratorConfigFragment newInstance(String param1, String param2) {
        FloatingPointGeneratorConfigFragment fragment = new FloatingPointGeneratorConfigFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    public FloatingPointGeneratorConfigFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment

        View result = inflater.inflate(R.layout.fragment_floating_point_generator_config, container, false);
        ButterKnife.bind(this, result);

        return result;
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        int generatorIndex = HomeFragment.lampConfig.getGeneratorIndex();

        HomeFragment.service.getGeneratorConfig(generatorIndex, new Callback<Map>() {
            @Override
            public void success(Map map, Response response) {
                generatorConfig = map;
                int minSpeed = ((Double) map.get("minSpeed")).intValue();
                int maxSpeed = ((Double) map.get("maxSpeed")).intValue();
                int maxPoints = ((Double) map.get("maxPoints")).intValue();
                int tailLength = ((Double) map.get("tailElementSpeedFactor")).intValue();
                seekBarMinSpeed.setProgress((minSpeed * 100) / MAX_SPEED);
                seekBarMaxSpeed.setProgress((maxSpeed * 100) / MAX_SPEED);
                seekBarMaxPoints.setProgress((maxPoints * 100) / MAX_POINTS);
                seekBarTailLength.setProgress((tailLength * 100) / MAX_TAIL_LENGTH);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e(TAG, "setConfig() failed ", error);
            }
        });

        seekBarMinSpeed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                if (progress > seekBarMaxSpeed.getProgress()) {
                    seekBarMaxSpeed.setProgress(progress);
                }
                updateConfig();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        seekBarMaxSpeed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                if (progress < seekBarMinSpeed.getProgress()) {
                    seekBarMinSpeed.setProgress(progress);
                }
                updateConfig();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        seekBarTailLength.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
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

        seekBarMaxPoints.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
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
        generatorConfig.put("minSpeed", seekBarMinSpeed.getProgress() * MAX_SPEED / 100);
        generatorConfig.put("maxSpeed", seekBarMaxSpeed.getProgress() * MAX_SPEED / 100);
        generatorConfig.put("maxPoints", seekBarMaxPoints.getProgress() * MAX_POINTS / 100);
        generatorConfig.put("tailElementSpeedFactor", seekBarTailLength.getProgress() * MAX_TAIL_LENGTH / 100);

        HomeFragment.service.setGeneratorConfig(HomeFragment.lampConfig.getGeneratorIndex(), generatorConfig, new Callback<Map>() {
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
