package de.tf.magiclamp.generator;

import android.app.Activity;
import android.os.Bundle;
import android.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.AdapterView;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import de.tf.magiclamp.Constants;
import de.tf.magiclamp.MagicLampService;
import de.tf.magiclamp.R;
import de.tf.magiclamp.model.GeneratorConfig;
import de.tf.magiclamp.model.GeneratorListAdapter;
import retrofit.Callback;
import retrofit.RestAdapter;
import retrofit.RetrofitError;
import retrofit.client.Response;

/**
 * A fragment representing a list of Items.
 * <p/>
 * Large screen devices (such as tablets) are supported by replacing the ListView
 * with a GridView.
 * <p/>
 * Activities containing this fragment MUST implement the {@link OnFragmentInteractionListener}
 * interface.
 */
public class GeneratorListFragment extends Fragment implements AbsListView.OnItemClickListener {

    MagicLampService service;

    private RecyclerView mRecyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager mLayoutManager;

    public static GeneratorListFragment newInstance() {
        GeneratorListFragment fragment = new GeneratorListFragment();
        Bundle args = new Bundle();
        fragment.setArguments(args);
        return fragment;
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public GeneratorListFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View view = inflater.inflate(R.layout.fragment_item, container, false);


        mRecyclerView = (RecyclerView) view.findViewById(R.id.generator_recycler_view);

        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        mRecyclerView.setHasFixedSize(true);

        // use a linear layout manager
        mLayoutManager = new LinearLayoutManager(this.getActivity());
        mRecyclerView.setLayoutManager(mLayoutManager);

        final List<GeneratorConfig> gc = new ArrayList<GeneratorConfig>();
        // specify an adapter (see also next example)
        mAdapter = new GeneratorListAdapter(gc);
        mRecyclerView.setAdapter(mAdapter);

        final Activity activity = getActivity();

        RestAdapter restAdapter = new RestAdapter.Builder()
                .setEndpoint(Constants.ML_URL)
                .build();
        service = restAdapter.create(MagicLampService.class);
        service.getGeneratorConfigList(new Callback<Map>() {
            @Override
            public void success(Map map, Response response) {

                int i = 0;
                for (Object item : map.values()) {
                    GeneratorConfig config = new GeneratorConfig();
                    Map itemMap = (Map) item;
                    config.setName(itemMap.get("name").toString());
                    config.setGeneratorIndex((int) Double.parseDouble(itemMap.get("generatorIndex").toString()));

                    gc.add(config);
                }

                mAdapter.notifyDataSetChanged();
            }

            @Override
            public void failure(RetrofitError error) {

            }
        });


        return view;
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
    }


    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p/>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        public void onFragmentInteraction(String id);
    }

}
